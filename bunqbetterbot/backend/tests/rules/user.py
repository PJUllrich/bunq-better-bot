import random

from model import EncryptedData, User
from tests.rules.base import BaseRule


class UserRule(BaseRule):
    @classmethod
    def create(cls):
        rand_chat_id = random.randint(1000, 1000000)
        rand_key_auth = EncryptedData(cls.faker.sha256().encode(), cls.faker.sha256().encode())
        rand_key_api = EncryptedData(cls.faker.sha256().encode(), cls.faker.sha256().encode())

        return User(rand_chat_id, rand_key_auth, rand_key_api)
