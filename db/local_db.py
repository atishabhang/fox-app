import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from constants import constants

Base = declarative_base()


def drop_database(db_name):
    try:
        os.remove(db_name)
    except OSError:
        pass


def create_database(db_name):
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    Base.metadata.create_all(engine)
    return engine
