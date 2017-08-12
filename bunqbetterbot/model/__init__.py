from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# _DB_URI = 'sqlite:////tmp/test.db'
_DB_URI = 'sqlite:///:memory:'

engine = create_engine(_DB_URI, convert_unicode=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()

from model.base_model import BaseModel
from model.user import User
from model.budget import Budget
from model.account_reference import AccountReference
from model.callback import Callback
from model.key import Key
from model.user_session import UserSession
from model.budget_result import BudgetResult
from model.account_alias import AccountAlias

Base.metadata.create_all(bind=engine)
