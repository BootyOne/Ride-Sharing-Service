from src.auth.models import User
from src.auth.schemas import UserUpdate, Token, UserCreate
from src.auth.utils import verify_password, get_password_hash, create_access_token, get_current_user, check_already_exists

from typing import Dict
from datetime import datetime

from pydantic import EmailStr
from peewee import DoesNotExist
from fastapi import Response, Request, APIRouter, HTTPException, Depends

router = APIRouter(
    prefix='/Auth',
    tags=['Auth']
)


@router.post("/login", response_model=Token)
async def login_for_access_token(response: Response, email: EmailStr, password: str):
    try:
        user = User.get(User.email == email)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": email})
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate):
    check_already_exists(user)

    hashed_password = get_password_hash(user.password)
    User.insert(
        username=user.username, email=user.email, hashed_password=hashed_password,
        first_name=user.first_name, second_name=user.second_name, requested_at=datetime.utcnow(), is_active=False
    ).execute()
    return user.model_dump()


@router.post("/logout")
async def logout_user(response: Response, request: Request):
    cookie_token = request.cookies.get("access_token")
    header_token = request.headers.get("Authorization")

    if not cookie_token and not header_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    response.delete_cookie(key="access_token")
    return {"detail": "Successfully logged out"}


@router.patch("/update", response_model=Dict)
async def update_user(user: UserUpdate, current_user: User = Depends(get_current_user)):
    query = User.update(**user.model_dump()).where(User.id == current_user.id)
    updated_rows = query.execute()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {'status': 'success'}
