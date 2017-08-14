from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base, BaseModel


class AccountReference(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    alias = relationship('AccountAlias', backref='account', uselist=False)
    callbacks = relationship('Callback', backref='account')

    def __init__(self, account):
        self.account_id = account.id_
        self.description = account.description
        self.alias = account.alias
        self.callbacks = []
