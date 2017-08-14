from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model import Base, BaseModel


class User(Base, BaseModel):
    env = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    key_api = Column(String, nullable=False)

    auth = relationship('Key', backref='user', uselist=False)
    accounts = relationship('AccountReference', backref='user')
    budgets = relationship('Budget', backref='user')

    def __init__(self, env, chat_id, key_auth, key_api):
        self.env = env
        self.chat_id = chat_id
        self.auth = key_auth
        self.key_api = key_api

        self.budgets = []
        self.accounts = []
