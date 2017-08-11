from telegram.ext import CallbackQueryHandler, ConversationHandler, Filters, MessageHandler, \
    RegexHandler

from telebot import msg
from telebot.conversation.base import Base, STATE
from telebot.conversation.register import BTS_ENV, Register

HOME_DECISION, ACCOUNT_DECISION, FUNCTION_DECISION, REGISTER, REGISTER_KEY, REGISTER_PW = range(6)

BTS_MAIN = ['Account', 'Functions']
BTS_ACCOUNT = ['Info', 'Login', '<< Back', 'Register']
BTS_FUNCTIONS = ['<< Back', 'Save the Cents', 'Budgets']


class Main(Base):
    def __init__(self, actions):
        Base.actions = actions
        self.setup_flow()

    @classmethod
    def setup_flow(cls):
        cls.btn_cmd_map = {
            HOME_DECISION: (BTS_MAIN, [cls.account, cls.functions]),
            ACCOUNT_DECISION: (BTS_ACCOUNT, [cls.info, cls.login, cls.home, cls.register]),
            FUNCTION_DECISION: (BTS_FUNCTIONS, [cls.home, cls.save_cents, cls.budgets])
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
                REGISTER: [CallbackQueryHandler(Register.environment, pass_user_data=True)],
                REGISTER_KEY: [MessageHandler(Filters.text, Register.api_key, pass_user_data=True)],
                REGISTER_PW: [MessageHandler(Filters.text, Register.password, pass_user_data=True)]
            },

            fallbacks=[]
        )

    @classmethod
    def home(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_MAIN)

        if update.callback_query is None:
            bot.send_message(update.message.chat_id, msg.HOME, reply_markup=markup)
        else:
            cls.edit_message(bot, update, msg.HOME, markup)

        user_data[STATE] = HOME_DECISION
        return HOME_DECISION

    @classmethod
    def account(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_ACCOUNT, col=2)

        cls.edit_message(bot, update, msg.ACCOUNT, markup)

        user_data[STATE] = ACCOUNT_DECISION
        return ACCOUNT_DECISION

    @classmethod
    def functions(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_FUNCTIONS, col=2, reverse=True)

        cls.edit_message(bot, update, msg.FUNCTIONS, markup)

        user_data[STATE] = FUNCTION_DECISION
        return FUNCTION_DECISION

    @classmethod
    def info(cls, bot, update, user_data):
        pass

    def login(self, bot, update, user_data):
        pass

    @classmethod
    def register(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_ENV, col=2)
        cls.edit_message(bot, update, msg.REGISTER_START + msg.REGISTER_ENV, markup=markup)

        return REGISTER

    @classmethod
    def save_cents(cls, bot, update, user_data):
        pass

    @classmethod
    def budgets(cls, bot, update, user_data):
        pass
