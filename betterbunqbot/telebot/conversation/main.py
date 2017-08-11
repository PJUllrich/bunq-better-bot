from telegram.ext import CallbackQueryHandler, ConversationHandler, RegexHandler

from telebot import msg
from telebot.conversation.base import BaseConversation, _STATE
from telebot.conversation.register import RegisterConversation, _BTS_ENV

HOME_DECISION, ACCOUNT_DECISION, FUNCTION_DECISION, REGISTER = range(4)

_BTS_MAIN = ['Account', 'Functions']
_BTS_ACCOUNT = ['Info', 'Login', '<< Back', 'Register']
_BTS_FUNCTIONS = ['<< Back', 'Save the Cents', 'Budgets']


class MainConversation(BaseConversation):
    def __init__(self, actions):
        BaseConversation.actions = actions
        self.setup_flow()

    @classmethod
    def setup_flow(cls):
        cls.btn_cmd_map = {
            HOME_DECISION: (_BTS_MAIN, [cls.account, cls.functions]),
            ACCOUNT_DECISION: (_BTS_ACCOUNT, [cls.info, cls.login, cls.home, cls.register]),
            FUNCTION_DECISION: (_BTS_FUNCTIONS, [cls.home, cls.save_cents, cls.budgets])
        }

    @property
    def handler(self):
        decision_handler = CallbackQueryHandler(self.decision, pass_user_data=True)

        return ConversationHandler(
            entry_points=[RegexHandler('\S*', self.home, pass_user_data=True)],

            states={
                HOME_DECISION: [decision_handler],
                ACCOUNT_DECISION: [decision_handler],
                FUNCTION_DECISION: [decision_handler],
                REGISTER: [RegisterConversation().handler]
            },

            fallbacks=[]
        )

    @classmethod
    def home(cls, bot, update, user_data):
        markup = cls.create_markup(_BTS_MAIN)

        if update.callback_query is None:
            bot.send_message(update.message.chat_id, msg.HOME, reply_markup=markup)
        else:
            cls.edit_message(bot, update, msg.HOME, markup)

        user_data[_STATE] = HOME_DECISION
        return HOME_DECISION

    @classmethod
    def account(cls, bot, update, user_data):
        markup = cls.create_markup(_BTS_ACCOUNT, col=2)

        cls.edit_message(bot, update, msg.ACCOUNT, markup)

        user_data[_STATE] = ACCOUNT_DECISION
        return ACCOUNT_DECISION

    @classmethod
    def functions(cls, bot, update, user_data):
        markup = cls.create_markup(_BTS_FUNCTIONS, col=2, reverse=True)

        cls.edit_message(bot, update, msg.FUNCTIONS, markup)

        user_data[_STATE] = FUNCTION_DECISION
        return FUNCTION_DECISION

    @classmethod
    def info(cls, bot, update, user_data):
        pass

    def login(self, bot, update, user_data):
        pass

    @classmethod
    def register(cls, bot, update, user_data):
        markup = cls.create_markup(_BTS_ENV, col=2)
        cls.edit_message(bot, update, msg.REGISTER_START + msg.REGISTER_ENV, markup=markup)

        return REGISTER

    @classmethod
    def save_cents(cls, bot, update, user_data):
        pass

    @classmethod
    def budgets(cls, bot, update, user_data):
        pass
