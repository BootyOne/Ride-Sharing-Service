from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.auth.schemas import UserUpdate
from src.auth.models import User, Role
from src.auth.utils import verify_password, get_password_hash, create_access_token
from peewee import DoesNotExist
from pydantic import BaseModel
from fastapi import Response, Request
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix='/Auth',
    tags=['Auth']
)



class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    second_name: str
    role_id: int


class RoleCreate(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, email: str, password: str):
    try:
        user = User.get(User.email == email)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": email})
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=UserCreate)
async def register_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    User.insert(role_id=1, username=user.username, email=user.email, hashed_password=hashed_password,
                    first_name=user.first_name, second_name=user.second_name, requested_at=datetime.utcnow(), is_active=False).execute()
    return user.model_dump()


@router.post("/logout/")
async def logout_user(response: Response, request: Request):
    cookie_token = request.cookies.get("access_token")
    header_token = request.headers.get("Authorization")

    if not cookie_token and not header_token:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    response.delete_cookie(key="access_token")
    return {"detail": "Successfully logged out"}


@router.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_obj = User(email=user.email, hashed_password=hashed_password)
    user_obj.save()
    return {"email": user.email, "password": hashed_password}


@router.post("/add_role/", response_model=RoleCreate)
async def register_user(role: RoleCreate):
    Role.insert(name=role.name).execute()
    return role.model_dump()


@router.patch("/users/{user_id}/", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    query = User.update(**user.dict()).where(User.id == user_id)
    updated_rows = query.execute()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return user.model_dump()
