from passlib.context import CryptContext
from jose import jwt
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict) -> str:
    return jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")
