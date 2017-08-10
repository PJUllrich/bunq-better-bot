from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_DB_URI = 'sqlite:///:memory:'

Base = declarative_base()

engine = create_engine(_DB_URI)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

from .user import User
from .budget import Budget
from .account import Account
from .callback import Callback
