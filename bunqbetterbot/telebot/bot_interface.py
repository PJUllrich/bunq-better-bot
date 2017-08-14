class BudgetInterface:
    @staticmethod
    def get_budget_updates():
        pass

    @staticmethod
    def create_budget(data):
        pass


class AccountInterface:
    @staticmethod
    def register(data):
        pass

    @staticmethod
    def login(data):
        pass


class BotInterface(BudgetInterface, AccountInterface):
    @staticmethod
    def get_active_accounts():
        pass

    @staticmethod
    def get_iban(account):
        pass
