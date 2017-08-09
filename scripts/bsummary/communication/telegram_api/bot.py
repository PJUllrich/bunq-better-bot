import logging

from bunq.sdk.model.generated import MonetaryAccountBank
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, \
    ConversationHandler, Filters, MessageHandler, Updater

from bsummary.communication.telegram_api import msg

logger = logging.getLogger(__name__)

_WEBHOOK_URL = 'YOUR URL HERE (e.g. www.example.com)'
_WEBHOOK_PATH = 'YOUR PATH HERE (e.g. telegram-bot'
CREATE_NAME, CREATE_IBAN, CREATE_DURATION, CREATE_KEYWORDS = range(4)
_INPUT_FINISH = 'END'

_WEBHOOK_PORT = 8525

_WEBHOOK_URLPATH = f'{_WEBHOOK_URL}/{_WEBHOOK_PATH}'


def owner_only(func):
    def inner(self, bot, update):
        if self.chat_id is not None and self.chat_id != update.message.chat_id:
            bot.send_message(update.message.chat_id, msg.NO_PERMISSION)
        else:
            return func(self, bot, update)

    return inner


class TelegramBot:
    def __init__(self, token, actions):
        self.chat_id = None
        self.creation = {}
        self.actions = actions

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.setup_handlers()

        self.setup_webhook()

    def setup_handlers(self):
        handler_start = CommandHandler('start', self.start)
        handler_update = CommandHandler('update', self.update)
        handler_create = self._get_create_handler()

        self.dispatcher.add_handler(handler_start)
        self.dispatcher.add_handler(handler_update)
        self.dispatcher.add_handler(handler_create)

        self.dispatcher.add_error_handler(self.error)

    def setup_webhook(self):
        self.updater.start_webhook(port=_WEBHOOK_PORT,
                                   url_path=_WEBHOOK_PATH,
                                   webhook_url=_WEBHOOK_URLPATH)
        self.updater.bot.set_webhook(url=_WEBHOOK_URLPATH)
        logger.info(f'Telegram bot is now listening on port {_WEBHOOK_PORT}.')

    @owner_only
    def start(self, bot, update):
        logger.info('/start command received')
        if self.chat_id is None:
            self.chat_id = update.message.chat_id

        bot.send_message(self.chat_id, msg.WELCOME)

    @owner_only
    def update(self, bot, update):
        logger.info('/update command received')

        bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)

        budget_results = self.actions.calc_budgets()
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

    @owner_only
    def create_start(self, bot, update):
        logger.info('Create: A new budget creation was started.')

        bot.send_message(update.message.chat_id, msg.CREATE_START)
        bot.send_message(update.message.chat_id, msg.CREATE_NAME)

        return CREATE_NAME

    @owner_only
    def create_name(self, bot, update):
        logger.info('Create: Received name of budget.')

        bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)

        self.creation['name'] = update.message.text
        accounts = self.actions.get_active_accounts()

        reply_markup = self._get_iban_keyboard(accounts)

        bot.send_message(update.message.chat_id, msg.CREATE_IBAN,
                         reply_markup=reply_markup)

        self.creation['IBANs'] = []

        return CREATE_IBAN

    @owner_only
    def create_iban(self, bot, update):
        data = update.callback_query.data

        if data == _INPUT_FINISH:
            return CREATE_DURATION

        self.creation['IBANs'].append(data)
        return CREATE_IBAN

    @owner_only
    def create_duration(self, bot, update):
        logger.info('Create: Received duration of budget.')

        reply_keyboard = [[1, 2, 3, 4, 'more']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                           one_time_keyboard=True)

    @owner_only
    def create_duration_more(self, bot, update):
        pass

    @owner_only
    def create_keywords(self, bot, update):
        pass

    @owner_only
    def create_cancel(self, bot, update):
        bot.send_message(self.chat_id, msg.CREATE_CANCEL)
        self.creation = {}

        return ConversationHandler.END

    def error(self, bot, update, error):
        logging.warning('Update "%s" caused error "%s"' % (update, error))

    def _get_create_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler('create', self.create_start)],

            states={
                CREATE_NAME: [MessageHandler(Filters.text, self.create_name)],
                CREATE_IBAN: [CallbackQueryHandler(self.create_iban)],
                CREATE_DURATION: [],
                CREATE_KEYWORDS: []
            },

            fallbacks=[CommandHandler('cancel', self.create_cancel)]

        )

    def _get_iban_keyboard(self, accounts):
        """

        Parameters
        ----------
        accounts    : list[MonetaryAccountBank]

        Returns
        -------

        """

        keyboard = []
        for acc in accounts:
            desc = acc.description
            IBAN = self.actions.get_iban(acc)
            button = InlineKeyboardButton(f'{desc}', callback_data=IBAN)
            keyboard.append([button])

        button_end = InlineKeyboardButton('Done', callback_data=_INPUT_FINISH)
        keyboard.append([button_end])
        return InlineKeyboardMarkup(keyboard)
