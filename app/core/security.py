from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    valid_password = pwd_context.verify(plain_password, hashed_password)
    return valid_password


def create_access_token(data: dict) -> str:
    return jwt.encode(
        {"sub": data["email"], "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )