from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    key = Column(String, nullable=False)
    budgets = relationship('Budget', backref='user', primaryjoin='User.id==Budget.user_id')
    accounts = relationship('Account', backref='user', primaryjoin='User.id==Account.user_id')

    def __init__(self, phone, password, key):
        self.phone = phone
        self.password = password
        self.key = key

        self.budgets = []
        self.accounts = []
