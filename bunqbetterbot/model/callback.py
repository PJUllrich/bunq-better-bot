from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from model import Base

_METHOD_URL = 'URL'


class Callback(Base):
    __tablename__ = 'callbacks'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', backref='callbacks')

    method = Column(String(10), nullable=False)
    target = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)

    def __init__(self, target, category):
        """
        Parameters
        ----------
        target      : str
            The target url for the POST callback notification.
        category    : str
            The category of the callback in all caps. Categories can be found
            here: https://doc.bunq.com/api/1/page/callbacks
        """
        self.method = _METHOD_URL
        self.target = target
        self.category = category
