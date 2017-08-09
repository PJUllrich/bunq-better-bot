import logging

from telegram.ext import CommandHandler, Updater

from bsummary.communication.telegram_api import msg

logger = logging.getLogger(__name__)

_WEBHOOK_URL = 'YOUR URL HERE (e.g. www.example.com)'
_WEBHOOK_PATH = 'YOUR PATH HERE (e.g. telegram-bot'
_WEBHOOK_PORT = 8525

_WEBHOOK_URLPATH = f'{_WEBHOOK_URL}/{_WEBHOOK_PATH}'


def owner_only(func):
    def inner(self, bot, update):
        if self.chat_id is not None and self.chat_id != update.message.chat_id:
            bot.send_message(update.message.chat_id, msg.NO_PERMISSION)
        else:
            func(self, bot, update)

    return inner


class Telegram:
    def __init__(self, token):
        self.chat_id = None
        self.update_action = None

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.setup_handlers()

        self.updater.start_webhook(port=_WEBHOOK_PORT,
                                   url_path=_WEBHOOK_PATH,
                                   webhook_url=_WEBHOOK_URLPATH)
        self.updater.bot.set_webhook(url=_WEBHOOK_URLPATH)
        logger.info(f'Telegram bot is now listening on port {_WEBHOOK_PORT}.')

    def setup_handlers(self):
        handler_start = CommandHandler('start', self.start)
        handler_update = CommandHandler('update', self.update)

        self.dispatcher.add_handler(handler_start)
        self.dispatcher.add_handler(handler_update)

    @owner_only
    def start(self, bot, update):
        logger.info('/start command received')
        if self.chat_id is None:
            self.chat_id = update.message.chat_id

        bot.send_message(self.chat_id, msg.WELCOME)

    @owner_only
    def update(self, bot, update):
        logger.info('/update command received')

        if self.update_action is None:
            logger.error('Update_action needs to be set before the update '
                         'command can be used.')
            return

        budget_results = self.update_action()
        for res in budget_results:
            duration = self._get_duration(res.budget.days_covered)

            ans = msg.UPDATE.format(abs(res.expense), res.budget.name, duration)

            bot.send_message(self.chat_id, ans)
            logger.info(f'Update answer - {ans}')

    @staticmethod
    def _get_duration(period):
        if period != 1:
            duration = f"in the last " \
                       f"{f'{period} days' if period > 1 else 'day'}"
        else:
            duration = "yesterday"
        return duration
