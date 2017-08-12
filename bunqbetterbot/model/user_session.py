from sqlalchemy import Column, DateTime, ForeignKey, Integer

from model import Base
from model.base_model import BaseModel


class UserSession(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))
    expiry = Column(DateTime, nullable=False)

    def __init__(self, expiry):
        self.expiry = expiry
