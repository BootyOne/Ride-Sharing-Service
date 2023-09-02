from pydantic import BaseModel


class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    first_name: str = None
    second_name: str = None
    phone_number: str = None
    about_me: str = None
    car_make: str = None
    car_number: str = None
    is_male: bool = None
