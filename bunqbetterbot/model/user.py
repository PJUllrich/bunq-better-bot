from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from model import Base
from model.base_model import BaseModel


class User(Base, BaseModel):
    env = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    password = Column(String, nullable=False)

    key_api_id = Column(Integer, ForeignKey('keys.id'))
    key_api = relationship('Key', foreign_keys=[key_api_id], backref=backref('user', uselist=False))

    key_encrypt_id = Column(Integer, ForeignKey('keys.id'))
    key_encrypt = relationship('Key', foreign_keys=[key_encrypt_id])

    user_session = relationship('UserSession', backref=backref('user', uselist=False))

    accounts = relationship('AccountReference', backref='user')
    budgets = relationship('Budget', backref='user')

    def __init__(self, env, chat_id, password_hash, key_api, key_encrypt):
        self.env = env
        self.chat_id = chat_id
        self.password = password_hash
        self.key_api = key_api
        self.key_encrypt = key_encrypt

        self.budgets = []
        self.accounts = []
