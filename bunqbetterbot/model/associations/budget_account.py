from sqlalchemy import Column, ForeignKey, Integer, Table

from model import Base

budget_account = Table('budgetaccount', Base.metadata,
                       Column('account_id', Integer, ForeignKey('accounts.id'), primary_key=True),
                       Column('budget_id', Integer, ForeignKey('budgets.id'), primary_key=True)
                       )
