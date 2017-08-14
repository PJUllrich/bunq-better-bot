import logging

from telegram.ext import Updater

from bot_interface import BotInterface
from conversation.main import Main
from run_bot import WEBHOOK_PATH, WEBHOOK_PORT, WEBHOOK_URL

logger = logging.getLogger(__name__)

_WEBHOOK_URLPATH = f'{WEBHOOK_URL}/{WEBHOOK_PATH}'


class TelegramBot:
    actions = BotInterface()

    def __init__(self, token):
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.setup_handlers()

        self.setup_webhook()

    def setup_handlers(self):
        handler_main = Main(self.actions).handler
        self.dispatcher.add_handler(handler_main)

        self.dispatcher.add_error_handler(self.error)

    def setup_webhook(self):
        self.updater.start_webhook(port=WEBHOOK_PORT,
                                   url_path=WEBHOOK_PATH,
                                   webhook_url=_WEBHOOK_URLPATH)
        self.updater.bot.set_webhook(url=_WEBHOOK_URLPATH)
        logger.info(f'Telegram bot is now listening on port {WEBHOOK_PORT}.')

    def error(self, bot, update, error):
        logger.warning(f'Error: {error} caused by Update: {update}')
