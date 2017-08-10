from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from model import Base


class Account(Base):
    __tablename__ = 'accounts'

    user_id = Column(Integer, ForeignKey('users.id'))

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    alias = Column(JSON, nullable=False)
    callbacks = relationship('Callback', backref='account',
                             primaryjoin='Account.id==Callback.account_id')

    def __init__(self, account):
        self.account_id = account.id_
        self.description = account.description
        self.alias = account.alias
        self.callbacks = []
