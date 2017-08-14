from sqlalchemy import Column, ForeignKey, Integer, String

from model import Base, BaseModel


class Key(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))

    key = Column(String, nullable=False)
    iv = Column(String, nullable=False)

    def __init__(self, key, iv=None):
        self.key = key
        self.iv = iv
