import api.util as util
from model.budget import Budget


class ApiInterface:
    @staticmethod
    def get_active_accounts():
        return util.get_active_accounts()

    @staticmethod
    def get_iban(account):
        return util.get_iban(account)


class BudgetApiInterface(ApiInterface):
    def __init__(self):
        self.budgets = None

    def calc_budgets(self):
        accounts = util.get_active_accounts()
        results = [b.calc_budget(accounts) for b in self.budgets]
        return results

    def create_budget(self, info):
        name = info.get('name')
        iban = info.get('iban')
        days = info.get('duration')

        if None in [name, iban, days]:
            raise ValueError()

        b = Budget(name, iban)
        b.duration = days

        self.budgets.append(b)
