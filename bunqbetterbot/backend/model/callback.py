from sqlalchemy import Column, ForeignKey, Integer, String

from model import Base, BaseModel

_METHOD_URL = 'URL'


class Callback(Base, BaseModel):
    account_id = Column(Integer, ForeignKey('accountreferences.id'))

    method = Column(String, nullable=False)
    target = Column(String, nullable=False)
    category = Column(String, nullable=False)

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
