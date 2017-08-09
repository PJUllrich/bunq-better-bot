import api.util as util


class ApiInterface:
    @staticmethod
    def get_active_accounts():
        return util.get_active_accounts()

    @staticmethod
    def get_iban(account):
        return util.get_iban(account)


class BudgetApiInterface(ApiInterface):
    def __init__(self, budgets):
        self.budgets = budgets

    def calc_budgets(self):
        accounts = util.get_active_accounts()
        results = [b.calc_budget(accounts) for b in self.budgets]
        return results
