import api.util as util
from func.save.callbacks import setup_callbacks

user = util.get_user()
accounts = util.get_all_accounts(user)
setup_callbacks(accounts, [])
print('Exit: All callbacks removed from all accounts')
