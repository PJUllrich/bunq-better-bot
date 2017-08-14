import random

from model import Key, User
from tests.rules.base import BaseRule


class UserRule(BaseRule):
    @classmethod
    def create(cls):
        rand_env = random.choice(['Sandbox', 'Production'])
        rand_chat_id = random.randint(1000, 1000000)
        rand_key_auth = Key(cls.faker.sha256(), cls.faker.sha256())
        rand_key_api = cls.faker.sha256()

        return User(rand_env, rand_chat_id, rand_key_auth, rand_key_api)
