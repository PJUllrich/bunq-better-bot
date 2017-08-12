from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from model import Base
from model.base_model import BaseModel


class AccountReference(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    _alias = relationship('AccountAlias', backref=backref('account', uselist=False))
    callbacks = relationship('Callback', backref='account')

    def __init__(self, account):
        self.account_id = account.id_
        self.description = account.description
        self._alias = [account.alias]
        self.callbacks = []

    @property
    def alias(self):
        return self._alias[0]

    @alias.setter
    def alias(self, val):
        self._alias[0] = val
