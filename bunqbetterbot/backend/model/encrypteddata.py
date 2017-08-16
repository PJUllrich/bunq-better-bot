from sqlalchemy import Column, ForeignKey, Integer, LargeBinary

from model import Base, BaseModel


class EncryptedData(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))

    value = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)

    def __init__(self, key, iv=None):
        self.value = key
        self.salt = iv
