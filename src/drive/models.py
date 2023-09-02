from src.auth.models import User
from src.database.config import BaseModelDB
from src.regions.models import Country, City
from src.database.database import database_proxy

from peewee import TextField, ForeignKeyField, PrimaryKeyField, DateTimeField, IntegerField


class TripsStatuses(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    name = TextField(null=False, unique=True)

    class Meta:
        database = database_proxy


class Trips(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    driver_id = ForeignKeyField(model=User)
    description = TextField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    departure_country = ForeignKeyField(model=Country)
    departure_city = ForeignKeyField(model=City)
    arrival_country = ForeignKeyField(model=Country)
    arrival_city = ForeignKeyField(model=City)
    status = ForeignKeyField(model=TripsStatuses)
    total_seats = IntegerField(default=4)
    reserved_seats = IntegerField(default=0)

    class Meta:
        database = database_proxy


class UserTrips(BaseModelDB):
    id = PrimaryKeyField(unique=True)
    trip_id = ForeignKeyField(model=Trips)
    user_id = ForeignKeyField(model=User)

    class Meta:
        database = database_proxy
