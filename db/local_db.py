import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from constants import constants

Base = declarative_base()


def drop_database():
    try:
        os.remove(constants.DB_NAME)
    except OSError:
        pass


def create_database():
    engine = create_engine(f"sqlite:///{constants.DB_NAME}", echo=False)
    Base.metadata.create_all(engine)
    return engine
