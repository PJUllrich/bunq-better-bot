from bunq.sdk import context

import api.util as util
import util.logger as logger
from api.client import Client
from bsummary.budget import Budget

_API_KEY = 'YOUR API KEY HERE'
_DEVICE_DESCRIPTION = 'YOUR DEVICE DESCRIPTION HERE'

# Change this one, once you're ready to leave the SandBox!
_ENVIRONMENT = context.ApiEnvironmentType.SANDBOX

# These are some example Budgets
budget_example_1 = Budget('Food', ['YOUR IBAN HERE', 'Optional: 2nd IBAN HERE'])
bugdet_example_2 = Budget('Another one', ['Another or same IBAN here'])

# This example budget covers the whole last week
bugdet_example_2.days_covered = 7

_BUDGETS = [
    budget_example_1,
    bugdet_example_2
]

if __name__ == "__main__":
    logger.setup_logger('output-budgetsummary.log')
    Client.setup_api_context(_ENVIRONMENT, _API_KEY, _DEVICE_DESCRIPTION)
    accounts = util.get_active_accounts()
    results = [b.calc_budget(accounts) for b in _BUDGETS]
    # Sent the results
