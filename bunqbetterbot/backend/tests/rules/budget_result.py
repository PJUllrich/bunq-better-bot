import random

from model import BudgetResult
from tests.rules.base import BaseRule


class BudgetResultRule(BaseRule):
    @classmethod
    def create(cls):
        return BudgetResult(random.random() * random.randint(1, 1000))
