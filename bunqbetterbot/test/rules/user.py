import random

from model import User
from test.rules.base import BaseRule


class UserRule(BaseRule):
    @classmethod
    def create(cls):
        rand_env = random.choice(['Sandbox', 'Production'])
        rand_chat_id = random.randint(1000, 1000000)
        rand_password = cls.faker.sha256()
        rand_api = f'"encrypted_key": {cls.faker.sha256()}, "iv": {cls.faker.sha256()}'
        rand_encrypt = f'"encrypted_key": {cls.faker.sha256()}, "iv": {cls.faker.sha256()}'

        return User(rand_env, rand_chat_id, rand_password, rand_api, rand_encrypt)
