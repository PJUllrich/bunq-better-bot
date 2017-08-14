from model import BudgetResult
from tests.rules.budget_result import BudgetResultRule
from tests.test_base import BaseTest


class BudgetResultTest(BaseTest):
    def test_create_budget_result(self):
        try:
            rand_budget_result = BudgetResultRule.create()
            BudgetResult.add(rand_budget_result)
            assert True
        except Exception as e:
            assert False, f'No Exception should be thrown. Exception: {str(e)}'
