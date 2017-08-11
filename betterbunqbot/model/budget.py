from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base, session


class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='budgets')

    name = Column(String(250), nullable=False)
    limit = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    history = Column(String)

    def __init__(self, user, name, limit, duration):
        self.user = user
        self.name = name
        self.limit = limit
        self.duration = duration

        self.history = ''

    @staticmethod
    def add_budget(budget):
        session.add(budget)
        session.commit()
