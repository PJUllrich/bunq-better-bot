from sqlalchemy import Column, ForeignKey, Integer, String

from model import Base, BaseModel


class Key(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))

    value = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    def __init__(self, key, iv=None):
        self.value = key
        self.salt = iv
