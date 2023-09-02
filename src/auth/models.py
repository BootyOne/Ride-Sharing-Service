from datetime import datetime
from src.database.config import BaseModel

from peewee import BooleanField, ForeignKeyField, DateTimeField, TextField, PrimaryKeyField
from src.database.database import database_proxy


class Role(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = TextField(unique=True, null=False)

    class Meta:
        database = database_proxy


class User(BaseModel):
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
    role_id = ForeignKeyField(column_name='role_id', model=Role)
    requested_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=False)

    class Meta:
        database = database_proxy
