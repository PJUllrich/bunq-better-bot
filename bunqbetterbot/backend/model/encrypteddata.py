from sqlalchemy import Column, ForeignKey, Integer, LargeBinary

from model import Base, BaseModel


class EncryptedData(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))

    value = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)

    def __init__(self, value, salt):
        """

        Parameters
        ----------
        value:  bytes
            The encrypted data in bytes format

        salt:   bytes
            The salt which is needed to decrypt the data
        """

        self.value = value
        self.salt = salt
