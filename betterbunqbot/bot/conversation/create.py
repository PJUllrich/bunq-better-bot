import logging

from telegram import ChatAction, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, \
    ConversationHandler, Filters, MessageHandler

from bot import msg
from bot.conversation.base import BaseConversation

logger = logging.getLogger(__name__)

NAME, IBAN, DURATION, DURATION_MORE = range(4)
_INPUT_DONE = 'Done'
_INPUT_MORE = 'More'


class CreateConversation(BaseConversation):
    def __init__(self, actions):
        self.actions = actions
        self.creation = {}

        self.handler = self._setup_handler()

    def _setup_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler('create', self.start)],

            states={
                NAME: [MessageHandler(Filters.text, self.get_name)],
                IBAN: [MessageHandler(Filters.text, self.get_iban)],
                DURATION: [MessageHandler(Filters.text, self.get_duration)],
                DURATION_MORE: [MessageHandler(Filters.text,
                                               self.get_duration_more)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]

        )

    def start(self, bot, update):
        logger.info('Create: A new budget creation was started.')

        bot.send_message(update.message.chat_id, msg.CREATE_START)
        bot.send_message(update.message.chat_id, msg.CREATE_NAME)

        return NAME

    def get_name(self, bot, update):
        logger.info('Create: Received name of budget.')

        self._send_typing(bot, update)

        self.creation['name'] = update.message.text

        accounts = self.actions.get_active_accounts()
        markup = self._get_keyboard_iban(accounts)

        bot.send_message(update.message.chat_id, msg.CREATE_IBAN,
                         reply_markup=markup)

        self.creation['iban'] = []

        return IBAN

    def get_iban(self, bot, update):
        logger.info('Create: Received an iban for budget.')
        data = update.message.text

        if data == _INPUT_DONE:
            self.creation['iban'] = list(set(self.creation['iban']))
            markup = self._get_keyboard_duration()
            bot.send_message(update.message.chat_id, msg.CREATE_DURATION,
                             reply_markup=markup)
            return DURATION

        iban = data.split(' - ')[1]
        self.creation['iban'].append(iban)

        return IBAN

    def get_duration(self, bot, update):
        logger.info('Create: Received duration of budget.')

        data = update.message.text

        if data == _INPUT_MORE:
            bot.send_message(update.message.chat_id, msg.CREATE_DURATION_MORE)
            return DURATION

        try:
            duration = int(data)
        except ValueError:
            bot.send_message(update.message.chat_id,
                             msg.INVALID_INPUT_NUMBER)
            return DURATION

        self.creation['duration'] = duration

        try:
            self._create_budget()
        except ValueError:
            bot.send_message(update.message.chat_id,
                             msg.INVALID_INPUT)
            return ConversationHandler.END

        return self.finish(bot, update)

    def get_duration_more(self, bot, update):
        pass

    def finish(self, bot, update):

        bot.send_message(update.message.chat_id, msg.CREATE_FINISH)

        return ConversationHandler.END

    def cancel(self, bot, update):
        bot.send_message(update.message.chat_id, msg.CANCEL)

        self.creation = {}

        return ConversationHandler.END

    def _get_keyboard_iban(self, accounts):
        """

        Parameters
        ----------
        accounts    : list[MonetaryAccountBank]

        Returns
        -------

        """

        keyboard = []
        for acc in accounts:
            iban = self.actions.get_iban(acc)
            button = KeyboardButton(f'{acc.description} - {iban}')
            keyboard.append([button])

        button_end = KeyboardButton(_INPUT_DONE)
        keyboard.append([button_end])

        return ReplyKeyboardMarkup(keyboard)

    @staticmethod
    def _get_keyboard_duration():
        keyboard = []
        for i in range(1, 9, 2):
            bts = [KeyboardButton(str(i)), KeyboardButton(str(i + 1))]
            keyboard.append(bts)

        button_more = KeyboardButton(_INPUT_MORE)
        keyboard.append([button_more])

        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        return markup

    @staticmethod
    def _send_typing(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)

    def _create_budget(self):
        self.actions.create_budget(self.creation)
        self.creation = {}
