"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Country(pw.Model):
        name = pw.TextField()

        class Meta:
            table_name = "country"

    @migrator.create_model
    class City(pw.Model):
        name = pw.TextField()
        latitude = pw.FloatField()
        longitude = pw.FloatField()
        country_id = pw.ForeignKeyField(column_name='country_id', field='id', model=migrator.orm['country'])

        class Meta:
            table_name = "city"

    @migrator.create_model
    class Role(pw.Model):
        name = pw.TextField(unique=True)

        class Meta:
            table_name = "role"

    @migrator.create_model
    class User(pw.Model):
        username = pw.TextField(unique=True)
        email = pw.TextField(unique=True)
        hashed_password = pw.TextField()
        first_name = pw.TextField()
        second_name = pw.TextField()
        phone_number = pw.TextField(null=True, unique=True)
        about_me = pw.TextField(null=True)
        car_make = pw.TextField(null=True)
        car_number = pw.TextField(null=True)
        is_male = pw.BooleanField(null=True)
        role_id = pw.ForeignKeyField(column_name='role_id', field='id', model=migrator.orm['role'])
        requested_at = pw.DateTimeField()
        is_active = pw.BooleanField(default=False)

        class Meta:
            table_name = "user"

    @migrator.create_model
    class Trips(pw.Model):
        driver = pw.ForeignKeyField(column_name='driver_id', field='id', model=migrator.orm['user'])
        description = pw.TextField()
        start_time = pw.DateTimeField()
        end_time = pw.DateTimeField()
        departure_country = pw.ForeignKeyField(column_name='departure_country_id', field='id', model=migrator.orm['country'])
        departure_city = pw.ForeignKeyField(column_name='departure_city_id', field='id', model=migrator.orm['city'])
        arrival_country = pw.ForeignKeyField(column_name='arrival_country_id', field='id', model=migrator.orm['country'])
        arrival_city = pw.ForeignKeyField(column_name='arrival_city_id', field='id', model=migrator.orm['city'])
        status = pw.BooleanField(default=False)
        total_seats = pw.IntegerField(default=4)
        reserved_seats = pw.IntegerField(default=0)

        class Meta:
            table_name = "trips"

    @migrator.create_model
    class TripsStatuses(pw.Model):
        name = pw.TextField(unique=True)

        class Meta:
            table_name = "tripsstatuses"

    @migrator.create_model
    class UserTrips(pw.Model):
        trip = pw.ForeignKeyField(column_name='trip_id', field='id', model=migrator.orm['trips'])

        class Meta:
            table_name = "usertrips"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('usertrips')

    migrator.remove_model('tripsstatuses')

    migrator.remove_model('trips')

    migrator.remove_model('user')

    migrator.remove_model('role')

    migrator.remove_model('city')

    migrator.remove_model('country')
