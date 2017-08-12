import random

from model import User, Key, session
from tests.rules.base import BaseRule


class UserRule(BaseRule):
    @classmethod
    def create(cls):
        rand_env = random.choice(['Sandbox', 'Production'])
        rand_chat_id = random.randint(1000, 1000000)
        rand_password = cls.faker.sha256()
        rand_api = Key(cls.faker.sha256(), cls.faker.sha256())
        rand_encrypt = Key(cls.faker.sha256())

        session.add_all([rand_api, rand_encrypt])

        return User(rand_env, rand_chat_id, rand_password, rand_api, rand_encrypt)
