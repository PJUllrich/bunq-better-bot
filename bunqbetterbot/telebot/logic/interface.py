import os
import requests

BACKEND_URL = os.environ['BUNQ_BOT_BACKEND_URL']


class BotInterface:
    @staticmethod
    def get_budget_updates():
        pass

    @staticmethod
    def create_budget(data):
        pass

    @staticmethod
    def register(data):
        return requests.post(BACKEND_URL + '/user/register', json=data)

    @staticmethod
    def login(data):
        return requests.post(BACKEND_URL + '/user/login', json=data)

    @staticmethod
    def get_active_accounts(data):
        return requests.get(BACKEND_URL + '/user/account/active', json=data)

    @staticmethod
    def get_iban(account):
        pass
