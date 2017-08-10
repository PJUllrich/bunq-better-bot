from sqlalchemy import Column, ForeignKey, Integer, Table

from model import Base

budget_account = Table('BudgetAccount', Base.metadata,
                       Column('budget_id', Integer, ForeignKey('budgets.id')),
                       Column('account_id', Integer, ForeignKey('accounts.id'))
                       )
