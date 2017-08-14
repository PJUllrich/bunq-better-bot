from sqlalchemy import Column, ForeignKey, Integer, String

from model import Base, BaseModel

_TYPE_IBAN = 'IBAN'


class AccountAlias(Base, BaseModel):
    account_id = Column(Integer, ForeignKey('accountreferences.id'))

    type_ = Column(String, nullable=False)
    value = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, value, name):
        self.type_ = _TYPE_IBAN
        self.value = value
        self.name = name
