import logging

from telegram.ext import CommandHandler, Updater

logger = logging.getLogger(__name__)

_MSG_WELCOME = "Hello there! I'll give you regular updates for your " \
               "bunq budgets!"
_MSG_NO_PERMISSION = "You don't have permission to contact this bot!"


def owner_only(func):
    def inner(self, bot, update):
        if self.chat_id is not None and self.chat_id != update.message.chat_id:
            bot.send_message(update.message.chat_id, _MSG_NO_PERMISSION)
        else:
            func(self, bot, update)

    return inner


class Telegram:
    def __init__(self, token, update_action):
        self.update_action = update_action
        self.chat_id = None

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.setup_handlers()

        logger.info('Telegram bot is now polling ...')
        self.updater.start_polling()

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

        bot.send_message(self.chat_id, _MSG_WELCOME)

    @owner_only
    def update(self, bot, update):
        logger.info('/update command received')

        budget_results = self.update_action()
        for res in budget_results:
            period = res.budget.days_covered
            if period != 1:
                duration = f"in the last " \
                           f"{f'{period} days' if period > 1 else 'day'}"
            else:
                duration = "yesterday"

            msg = f"You spent {abs(res.expense)} Euro of your " \
                  f"{res.budget.name} budget {duration}"

            logger.info(f'Update result - {msg}')
            bot.send_message(self.chat_id, msg)
