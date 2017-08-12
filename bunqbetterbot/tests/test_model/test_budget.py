from model import Budget
from tests.rules.budget import BudgetRule
from tests.rules.user import UserRule
from tests.test_base import BaseTest


class BudgetTest(BaseTest):
    def test_create_budget(self):
        try:
            rand_user = UserRule.create()
            budget_new = BudgetRule.create(rand_user)
            Budget.add(budget_new)
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
