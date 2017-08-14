from model import Callback
from tests.rules.base import BaseRule


class CallbackRule(BaseRule):
    @classmethod
    def create(cls):
        rand_target = cls.faker.uri()
        rand_category = cls.faker.name()

        return Callback(rand_target, rand_category)
