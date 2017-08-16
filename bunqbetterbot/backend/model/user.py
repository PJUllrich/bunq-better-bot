from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from model import Base, BaseModel


class User(Base, BaseModel):
    chat_id = Column(Integer, nullable=False)

    auth_id = Column(Integer, ForeignKey('encrypteddatas.id'))
    auth = relationship('EncryptedData', foreign_keys=[auth_id], backref='user', uselist=False)

    api_conf_id = Column(Integer, ForeignKey('encrypteddatas.id'))
    api_conf = relationship('EncryptedData', foreign_keys=[api_conf_id])

    accounts = relationship('AccountReference', backref='user')
    budgets = relationship('Budget', backref='user')

    def __init__(self, chat_id, auth, api_conf):
        """

        Parameters
        ----------
        chat_id:    int
            Unique identifier of the chat between bot and user

        auth:       EncryptedData
            User password hash for authentication and salt to retrieve the authentication and
            encryption hashes from clear Password

        api_conf:   EncryptedData
            Encrypted JSON string representation of an ApiContext instance and salt to decrypt it
        """

        self.chat_id = chat_id

        self.auth = auth
        self.api_conf = api_conf

        self.budgets = []
        self.accounts = []
