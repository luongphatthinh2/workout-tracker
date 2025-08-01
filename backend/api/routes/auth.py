from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserOut, ChangePasswordRequest
from query import user as crud_user
from core import security
from db.session import get_db_session
from fastapi import Request
from models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    user = await crud_user.get_user_by_username(db, user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = await crud_user.create_user(db, user_in)
    return new_user

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    user = await crud_user.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = security.create_access_token(request=request, data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password", summary="Change your password", status_code=200)
async def change_password(
    data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(crud_user.get_current_user),
):
    # Step 1: Verify current password is correct
    if not security.verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current password is incorrect"
        )

    # Step 2: Hash the new password
    new_hashed = security.get_password_hash(data.new_password)

    # Step 3: Update password in the database
    await crud_user.update_user_password(db, current_user.id, new_hashed)

    return {"detail": "Password changed successfully"}