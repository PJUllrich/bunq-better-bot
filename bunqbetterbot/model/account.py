from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base


class Account(Base):
    __tablename__ = 'accounts'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='accounts')

    # budgets = relationship("Budget",
    #                        secondary=budget_account,
    #                        backref="accounts")

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    alias = Column(String, nullable=False)

    def __init__(self, account):
        self.account_id = account.id_
        self.description = account.description
        self.alias = account.alias
        self.callbacks = []
