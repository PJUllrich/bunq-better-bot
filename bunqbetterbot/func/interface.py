import api.util as util
from func import account, budget


class BudgetInterface:
    @staticmethod
    def get_budget_updates():
        return budget.get_updates()

    @staticmethod
    def create_budget(data):
        return budget.create(data)


class AccountInterface:
    @staticmethod
    def register(data):
        return account.register(data)

    @staticmethod
    def login(data):
        return account.login(data)


class Interface(BudgetInterface, AccountInterface):
    @staticmethod
    def get_active_accounts():
        return util.get_active_accounts()

    @staticmethod
    def get_iban(account):
        return util.get_iban(account)
