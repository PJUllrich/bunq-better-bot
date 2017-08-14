from model import Key
from tests.rules.base import BaseRule


class KeyRule(BaseRule):
    @classmethod
    def create(cls):
        rand_key = cls.faker.sha256().encode()
        rand_iv = cls.faker.sha256().encode()
        rand_iv = rand_iv[:(len(rand_iv) // 2)]

        return Key(rand_key, rand_iv)
