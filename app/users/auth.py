from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=15)
    to_encode.update({"exp": expire})
    auth_data = settings.get_auth_data
    return jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])

async def authenticate_user(user, password):
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user