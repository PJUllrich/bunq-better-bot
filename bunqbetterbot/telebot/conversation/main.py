from telegram.ext import CallbackQueryHandler, ConversationHandler, Filters, MessageHandler, \
    RegexHandler

from telebot import msg
from telebot.conversation.base import Base, STATE
from telebot.conversation.login import Login
from telebot.conversation.register import Register

HOME_DECISION, ACCOUNT_DECISION, FUNCTION_DECISION, \
REGISTER_ENV, REGISTER_KEY, REGISTER_PW, \
LOGIN_PW, LOGIN_DEL = range(8)

BTS_MAIN = ['Account', 'Functions']
BTS_ACCOUNT = ['Info', 'Login', '<< Back', 'Register']
BTS_FUNCTIONS = ['<< Back', 'Save the Cents', 'Budgets']
BTS_DELETE_MSG = ["I don't know how", "Done"]


class Main(Base):
    def __init__(self, actions):
        Base.actions = actions
        self.setup_flow()

    @classmethod
    def setup_flow(cls):
        cls.btn_cmd_map = {
            HOME_DECISION: (BTS_MAIN, [cls.account, cls.functions]),
            ACCOUNT_DECISION: (BTS_ACCOUNT, [cls.info, Login.start, cls.home, Register.start]),
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
                REGISTER_ENV: [CallbackQueryHandler(Register.environment, pass_user_data=True)],
                REGISTER_KEY: [MessageHandler(Filters.text, Register.api_key, pass_user_data=True)],
                REGISTER_PW: [MessageHandler(Filters.text, Register.password, pass_user_data=True)],
                LOGIN_PW: [MessageHandler(Filters.text, Login.password, pass_user_data=True)],
                LOGIN_DEL: [CallbackQueryHandler(Login.delete, pass_user_data=True)]
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

    @classmethod
    def save_cents(cls, bot, update, user_data):
        pass

    @classmethod
    def budgets(cls, bot, update, user_data):
        pass
