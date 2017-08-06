from bunq.sdk import context

import api
import util
from callbacks import Callback, setup_callbacks
from handler.balance_rounding import BalanceRoundingHandler
from handler.platform import EventHandlerPlatform
from listener import start_event_listener
from logger import setup_logger

# Set these parameters and you're ready to go!
_API_KEY = 'YOUR API KEY HERE'
_DEVICE_DESCRIPTION = 'YOUR DEVICE DESCRIPTION HERE'
_CALLBACK_URL = 'YOUR CALLBACK URL HERE (MUST BE HTTPS)'
_SAVINGS_IBAN = 'THE IBAN TO YOUR SAVINGS ACCOUNT HERE'

# If you want to add more callbacks to your accounts, add them as Callback
# instances here with category and url
_PINSPAREN_CALLBACK = 'MUTATION'
_CALLBACKS = [
    Callback(_PINSPAREN_CALLBACK, _CALLBACK_URL)
]

# Change this to PRODUCTION once you're ready to leave the sandbox!
_ENVIRONMENT = context.ApiEnvironmentType.PRODUCTION

# Change this port if it overlaps with another port on your system
_PORT = 8500

if __name__ == "__main__":
    setup_logger()
    api.Client.setup_api_context(_ENVIRONMENT, _API_KEY, _DEVICE_DESCRIPTION)

    balance_rounding_handler = BalanceRoundingHandler(_SAVINGS_IBAN)
    EventHandlerPlatform.add_handler(balance_rounding_handler,
                                     _PINSPAREN_CALLBACK)

    active_accounts_wo_savings = [acc for acc in util.get_active_accounts()
                                  if util.get_iban(acc) != _SAVINGS_IBAN]
    setup_callbacks(active_accounts_wo_savings, _CALLBACKS)

    start_event_listener(_PORT)
