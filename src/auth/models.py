from src.database.config import BaseModelDB
from src.database.database import database_proxy

from datetime import datetime

from peewee import BooleanField, DateTimeField, TextField, PrimaryKeyField


class User(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    username = TextField(unique=True, null=False)
    email = TextField(unique=True, null=False)
    hashed_password = TextField()
    first_name = TextField(null=False)
    second_name = TextField(null=False)
    phone_number = TextField(unique=True, null=True)
    about_me = TextField(null=True)
    car_make = TextField(null=True)
    car_number = TextField(null=True)
    is_male = BooleanField(null=True)
    requested_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=False)

    class Meta:
        database = database_proxy
