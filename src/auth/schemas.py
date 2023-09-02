from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr
    first_name: str = None
    second_name: str = None
    phone_number: str = None
    about_me: str = None
    car_make: str = None
    car_number: str = None
    is_male: bool = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    second_name: str
    role_id: int
    phone_number: str


class RoleCreate(BaseModel):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str
