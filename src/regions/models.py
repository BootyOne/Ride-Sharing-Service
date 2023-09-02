from peewee import TextField, ForeignKeyField, FloatField, PrimaryKeyField
from src.database.database import database_proxy
from src.database.config import BaseModelDB


class Country(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    name = TextField(null=False)

    class Meta:
        database = database_proxy


class City(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    name = TextField(null=False)
    latitude = FloatField(null=False)
    longitude = FloatField(null=False)
    country_id = ForeignKeyField(model=Country)

    class Meta:
        database = database_proxy
