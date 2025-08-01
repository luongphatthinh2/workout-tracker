from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from db.session import get_db_session

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_pw = get_password_hash(user_in.password)
    new_user = User(email=user_in.email, username=user_in.username, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Extract token from Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
    
) -> User:
    # Load config from app container
    config = request.app.container.config()

    # Define error to raise if token is invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode the JWT
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    return user

async def update_user_password(db: AsyncSession, user_id: int, new_hashed_password: str):
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(hashed_password=new_hashed_password)
    )
    await db.commit()
