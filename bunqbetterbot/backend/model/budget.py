from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base, BaseModel


class Budget(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))

    active = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    results = relationship('BudgetResult', backref='budget')

    def __init__(self, user, name, limit, duration):
        self.user = user

        self.active = True
        self.name = name
        self.limit = limit
        self.duration = duration

        self.results = []
