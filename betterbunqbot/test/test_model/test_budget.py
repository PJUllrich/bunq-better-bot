from model import Budget
from test.rules.budget import BudgetRule
from test.rules.user import UserRule
from test.test_base import BaseTest


class BudgetTest(BaseTest):
    def test_create_budget(self):
        rand_user = UserRule.create()
        budget_new = BudgetRule.create(rand_user)

        try:
            Budget.add_budget(budget_new)
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
