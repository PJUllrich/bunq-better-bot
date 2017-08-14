from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model import Base, BaseModel


class User(Base, BaseModel):
    env = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)

    key_auth_id = Column(Integer, ForeignKey('keys.id'))
    key_auth = relationship('Key', foreign_keys=[key_auth_id],
                            backref='user', uselist=False)

    key_api_id = Column(Integer, ForeignKey('keys.id'))
    key_api = relationship('Key', foreign_keys=[key_api_id])

    accounts = relationship('AccountReference', backref='user')
    budgets = relationship('Budget', backref='user')

    def __init__(self, env, chat_id, key_auth, key_api):
        self.env = env
        self.chat_id = chat_id

        self.key_auth = key_auth
        self.key_api = key_api

        self.budgets = []
        self.accounts = []
