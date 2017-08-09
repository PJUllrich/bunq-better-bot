import logging
import os

from telegram.ext import Updater

from bot.conversation.main import MainConversation

logger = logging.getLogger(__name__)

_WEBHOOK_URL = os.environ['BUNQ_BOT_URL']
_WEBHOOK_PATH = os.environ['BUNQ_BOT_URL_PATH']
_WEBHOOK_PORT = 8525

_WEBHOOK_URLPATH = f'{_WEBHOOK_URL}/{_WEBHOOK_PATH}'


class TelegramBot:
    def __init__(self, token, actions):
        self.actions = actions

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.setup_handlers()

        self.setup_webhook()

    def setup_handlers(self):
        handler_main = MainConversation().handler
        self.dispatcher.add_handler(handler_main)

        self.dispatcher.add_error_handler(self.error)

    def setup_webhook(self):
        self.updater.start_webhook(port=_WEBHOOK_PORT,
                                   url_path=_WEBHOOK_PATH,
                                   webhook_url=_WEBHOOK_URLPATH)
        self.updater.bot.set_webhook(url=_WEBHOOK_URLPATH)
        logger.info(f'Telegram bot is now listening on port {_WEBHOOK_PORT}.')

    def error(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"' % (update, error))

        # def update(self, bot, update):
        #     logger.info('/update command received')
        #
        #     bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)
        #
        #     budget_results = self.actions.calc_budgets()
        #     for res in budget_results:
        #         duration = self._get_duration(res.budget.days_covered)
        #
        #         ans = msg.UPDATE.format(abs(res.expense), res.budget.name, duration)
        #
        #         bot.send_message(self.chat_id, ans)
        #         logger.info(f'Update answer - {ans}')
        #
        # @staticmethod
        # def _get_duration(period):
        #     if period != 1:
        #         duration = f"in the last " \
        #                    f"{f'{period} days' if period > 1 else 'day'}"
        #     else:
        #         duration = "yesterday"
        #     return duration
