from sqlalchemy import Column, Integer, String

from model import Base, session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    env = Column(String, nullable=False)
    chat_id = Column(String, nullable=False)
    password = Column(String, nullable=False)
    key_api = Column(String, nullable=False)
    key_encrypt = Column(String, nullable=False)

    def __init__(self, env, chat_id, password_hash, key_api, key_encrypt):
        self.env = env
        self.chat_id = chat_id
        self.password = password_hash
        self.key_api = key_api
        self.key_encrypt = key_encrypt

        self.budgets = []
        self.accounts = []

    @staticmethod
    def add_user(user):
        session.add(user)
        session.commit()
