from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func

from model import Base, BaseModel


class BudgetResult(Base, BaseModel):
    budget_id = Column(Integer, ForeignKey('budgets.id'))

    created = Column(DateTime, default=func.now(), nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, amount):
        self.amount = amount
