from src.auth.models import User
from src.config import SECRET_KEY, ALGORITHM
from src.auth.schemas import UserCreate, UserUpdate

from typing import Union
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt
from peewee import DoesNotExist
from fastapi import HTTPException, Request


ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(request: Request) -> dict:
    cookie_token = request.cookies.get("access_token")
    header_token = request.headers.get("Authorization")

    if not cookie_token and not header_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    if header_token:
        actual_token = header_token.replace("Bearer ", "")
    else:
        actual_token = cookie_token

    payload = decode_access_token(actual_token)

    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    email = payload.get("sub")
    try:
        user = User.get(User.email == email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def check_already_exists(user: Union[UserCreate, UserUpdate]):
    fields = {
        "email": "User with this email already exists",
        "phone_number": "User with this phone already exists",
        "username": "User with this username already exists",
    }

    for field, error_message in fields.items():
        existing_user = User.select().where(getattr(User, field) == getattr(user, field)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail=error_message)
