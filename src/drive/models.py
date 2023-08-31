from peewee import Model, CharField, ForeignKeyField, BooleanField
from src.database.database import database_proxy
from src.auth.models import User

class Drive(Model):
    origin = CharField()
    destination = CharField()
    driver = ForeignKeyField(User, backref='drives')
    is_confirmed = BooleanField(default=False)

    class Meta:
        database = database_proxy
