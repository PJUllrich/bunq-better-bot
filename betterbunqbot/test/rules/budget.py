import random

from model import Budget
from test.rules.base import BaseRule


class BudgetRule(BaseRule):
    @classmethod
    def create(cls, user):
        rand_name = cls.faker.name()
        rand_limit = random.random() * random.randint(1, 1000)
        rand_duration = random.randint(1, 10)

        return Budget(user, rand_name, rand_limit, rand_duration)
