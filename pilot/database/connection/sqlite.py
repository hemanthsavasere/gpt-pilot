from peewee import SqliteDatabase
from pilot.database.config import DB_NAME


def get_sqlite_database():
    return SqliteDatabase(DB_NAME)
