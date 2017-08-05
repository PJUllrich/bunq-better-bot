from bunq.sdk import context

from api import setup_api_context
from balance_rounding import round_account_balances, set_savings_account
from callbacks import setup_callbacks
from handler import add_event_handler
from listener import start_event_listener
from logger import setup_logger

# Set these parameters and you're ready to go!
_API_KEY = 'YOUR API KEY HERE'
_DEVICE_DESCRIPTION = 'YOUR DEVICE DESCRIPTION HERE'
_CALLBACK_URL = 'YOUR CALLBACK URL HERE (MUST BE HTTPS)'
_SAVINGS_IBAN = 'THE IBAN TO YOUR SAVINGS ACCOUNT HERE'

# If you want to trigger automatic balance rounding when a callback from
# another category than MUTATION is created, change the following
_CALLBACK_CATEGORY = 'MUTATION'

# Change this to PRODUCTION once you're ready to leave the sandbox!
_ENVIRONMENT = context.ApiEnvironmentType.SANDBOX

# Change this port if it overlaps with another port on your system
_PORT = 8500

if __name__ == "__main__":
    setup_logger()
    setup_api_context(_ENVIRONMENT, _API_KEY, _DEVICE_DESCRIPTION)
    set_savings_account(_SAVINGS_IBAN)
    add_event_handler(_CALLBACK_CATEGORY, round_account_balances)
    setup_callbacks(_SAVINGS_IBAN, _CALLBACK_URL, _CALLBACK_CATEGORY)
    start_event_listener(_PORT)
