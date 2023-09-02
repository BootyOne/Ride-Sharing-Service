from peewee import TextField, ForeignKeyField, BooleanField, PrimaryKeyField, DateTimeField, IntegerField
from src.database.database import database_proxy
from src.auth.models import User
from src.regions.models import Country, City
from src.database.config import BaseModel


class TripsStatuses(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = TextField(null=False, unique=True)

    class Meta:
        database = database_proxy


class Trips(BaseModel):
    id = PrimaryKeyField(unique=True)
    driver = ForeignKeyField(User, backref='drives')
    description = TextField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    departure_country = ForeignKeyField(model=Country)
    departure_city = ForeignKeyField(model=City)
    arrival_country = ForeignKeyField(model=Country)
    arrival_city = ForeignKeyField(model=City)
    status = BooleanField(default=False)
    total_seats = IntegerField(default=4)
    reserved_seats = IntegerField(default=0)

    class Meta:
        database = database_proxy


class UserTrips(BaseModel):
    id = PrimaryKeyField(unique=True)
    trip = ForeignKeyField(model=Trips)

    class Meta:
        database = database_proxy
