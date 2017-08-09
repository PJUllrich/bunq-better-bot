import os
from bunq.sdk import context

import util.logger as logger
from api.client import Client
from bot.bot import TelegramBot
from model.budget import BudgetApiInterface

_API_KEY = os.environ['BUNQ_BOT_API_KEY']
_BOT_TOKEN = os.environ['BUNQ_BOT_TOKEN']
_DEVICE_DESCRIPTION = 'Better Bunq Bot'
_LOG_FILENAME = 'better-bunq-bot.log'

# Change this one, once you're ready to leave the SandBox!
_ENVIRONMENT = context.ApiEnvironmentType.PRODUCTION

if __name__ == "__main__":
    logger.setup_logger(_LOG_FILENAME)
    Client.setup_api_context(_ENVIRONMENT, _API_KEY, _DEVICE_DESCRIPTION)

    budget_interface = BudgetApiInterface()
    bot = TelegramBot(_BOT_TOKEN, budget_interface)
