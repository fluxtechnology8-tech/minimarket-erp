from core.database import Database


def init_db():
    db = Database()
    return db


def get_db():
    return Database()
