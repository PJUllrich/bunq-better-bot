from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from model import session


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id = Column(Integer, primary_key=True)

    @staticmethod
    def add(obj):
        session.add(obj)
        session.commit()

    @staticmethod
    def delete(obj):
        session.delete(obj)
        session.commit()

    @classmethod
    def qry_by(cls, condition, val):
        return cls.query.filter_by(**{condition: val})
