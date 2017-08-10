from sqlalchemy import Column, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from model import Base
from model.associations.budget_account import budget_account


class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    accounts = relationship('Account', secondary=budget_account, backref='budgets')

    name = Column(String(250), nullable=False)
    limit = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    history = Column(JSON)

    def __init__(self, name, accounts, limit, duration):
        self.name = name
        self.accounts = accounts
        self.limit = limit
        self.duration = duration

        self.history = []

    @staticmethod
    def add_budget(budget):
        pass
