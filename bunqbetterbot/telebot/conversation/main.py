from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Filters, \
    MessageHandler, RegexHandler

import conversation
import msg
import msg.general
import msg.main
from conversation.login import Login
from conversation.register import Register
from conversation.savethecents import SaveTheCents
from util import const

(HOME_DECISION, ACCOUNT_DECISION, FUNCTION_DECISION,
 REGISTER_ENV, REGISTER_KEY, REGISTER_PW,
 LOGIN_PW, LOGIN_DEL,
 SAVE_SAVING, SAVE_ACCOUNTS) = range(9)

BTS_MAIN = ['Account', 'Functions']
BTS_ACCOUNT = ['Info', 'Login', '<< Back', 'Register']
BTS_FUNCTIONS = ['<< Back', 'Save the Cents', 'Budgets']
BTS_DELETE_MSG = ["I don't know how", "Done"]


class Main(conversation.Base):
    def __init__(self):
        self.setup_flow()

    @classmethod
    def setup_flow(cls):
        cls.btn_cmd_map = {
            HOME_DECISION: (BTS_MAIN, [cls.account, cls.functions]),
            ACCOUNT_DECISION: (BTS_ACCOUNT, [cls.info, Login.start, cls.home, Register.start]),
            FUNCTION_DECISION: (BTS_FUNCTIONS, [cls.home, SaveTheCents.start, cls.budgets])
        }

    @property
    def handler(self):
        decision_handler = CallbackQueryHandler(self.decision, pass_user_data=True)
        cancel_handler = CommandHandler('cancel', self.cancel, pass_user_data=True)

        return ConversationHandler(
            entry_points=[RegexHandler('\S*', self.home, pass_user_data=True)],

            states={
                HOME_DECISION: [decision_handler],
                ACCOUNT_DECISION: [decision_handler],
                FUNCTION_DECISION: [decision_handler],

                REGISTER_ENV: [CallbackQueryHandler(Register.environment, pass_user_data=True)],
                REGISTER_KEY: [MessageHandler(Filters.text, Register.api_key, pass_user_data=True)],
                REGISTER_PW: [MessageHandler(Filters.text, Register.password, pass_user_data=True)],

                LOGIN_PW: [MessageHandler(Filters.text, Login.password, pass_user_data=True,
                                          edited_updates=True)],
                LOGIN_DEL: [CallbackQueryHandler(Login.delete, pass_user_data=True)]
            },

            fallbacks=[cancel_handler]
        )

    @classmethod
    def home(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_MAIN)

        if update.callback_query is None:
            user_data[const.CHAT_ID] = update.message.chat_id
            bot.send_message(update.message.chat_id, msg.main.HOME, reply_markup=markup)
        else:
            cls.edit_message(bot, update, msg.main.HOME, markup)

        user_data[const.USER_STATE] = HOME_DECISION
        return HOME_DECISION

    @classmethod
    def account(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_ACCOUNT, col=2)

        cls.edit_message(bot, update, msg.main.ACCOUNT, markup)

        user_data[const.USER_STATE] = ACCOUNT_DECISION
        return ACCOUNT_DECISION

    @classmethod
    def functions(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_FUNCTIONS, col=2, reverse=True)

        cls.edit_message(bot, update, msg.main.FUNCTIONS, markup)

        user_data[const.USER_STATE] = FUNCTION_DECISION
        return FUNCTION_DECISION

    @classmethod
    def cancel(cls, bot, update, user_data):
        cls.reset_user_data(update, user_data)

        markup = cls.create_markup(BTS_MAIN)
        bot.send_message(update.message.chat_id, msg.general.CANCEL, reply_markup=markup)

        user_data[const.USER_STATE] = HOME_DECISION
        return HOME_DECISION

    @staticmethod
    def reset_user_data(update, user_data):
        user_data.clear()
        user_data[const.CHAT_ID] = update.message.chat_id

    @classmethod
    def info(cls, bot, update, user_data):
        pass

    @classmethod
    def budgets(cls, bot, update, user_data):
        pass
