from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# _DB_URI = 'sqlite:////tmp/test.db'
_DB_URI = 'sqlite:///:memory:'

engine = create_engine(_DB_URI, convert_unicode=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from .base_model import BaseModel
from .account_alias import AccountAlias
from .budget_result import BudgetResult
from .key import Key
from .callback import Callback
from .user import User
from .account_reference import AccountReference
from .budget import Budget

Base.metadata.create_all(bind=engine)
