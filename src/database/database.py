from src.config import DB_USER, DB_PORT, DB_NAME, DB_HOST, DB_PASSWORD

from peewee import PostgresqlDatabase


database_proxy = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    autorollback=True,
)
