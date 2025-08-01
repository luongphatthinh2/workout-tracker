from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Request, Depends


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(request: Request, data: dict, expires_delta: timedelta = None):
    config = request.app.container.config()
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

def decode_access_token(token: str, request: Request):
    config = request.app.container.config()
    try:
        payload = jwt.decode(token,  config.secret_key, algorithms=[config.algorithm])
        return payload.get("sub")
    except JWTError:
        return None
