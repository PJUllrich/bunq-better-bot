from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User:
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    apikey = Column(String, nullable=False)
    budget = relationship('Budget')

    def __init__(self, phone, pw_hash, api_key):
        self.phone = phone
        self.password = pw_hash
        self.api_key = api_key

        self.budgets = None
        self.callbacks = None
