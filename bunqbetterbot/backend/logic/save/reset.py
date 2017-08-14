import api.util as util

from backend.func.save import setup_callbacks

user = util.get_user()
accounts = util.get_all_accounts(user)
setup_callbacks(accounts, [])
print('Exit: All callbacks removed from all accounts')
