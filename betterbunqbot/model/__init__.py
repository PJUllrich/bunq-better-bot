from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

_DB_URI = 'sqlite:////tmp/test.db'

engine = create_engine(_DB_URI, convert_unicode=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from model.user import User
from model.budget import Budget
from model.account import Account
from model.callback import Callback

Base.metadata.create_all(bind=engine)
