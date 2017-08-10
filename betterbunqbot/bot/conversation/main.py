from telegram.ext import CallbackQueryHandler, ConversationHandler, RegexHandler

from bot import msg
from bot.conversation.base import BaseConversation

_STATE = 'STATE'

HOME_DECISION, ACCOUNT_DECISION, FUNCTION_DECISION = range(3)

_BTS_MAIN = ['Account', 'Functions']
_BTS_ACCOUNT = ['Info', 'Login', '<< Back', 'Register']
_BTS_FUNCTIONS = ['<< Back', 'Save the Cents', 'Budgets']


class MainConversation(BaseConversation):
    def __init__(self):
        self.bts_cmds = self.setup_decisions()

    def setup_decisions(self):
        return {
            HOME_DECISION: (_BTS_MAIN, [self.account, self.functions]),
            ACCOUNT_DECISION: (_BTS_ACCOUNT, [self.info, self.login, self.home, self.register]),
            FUNCTION_DECISION: (_BTS_FUNCTIONS, [self.home, self.save_cents, self.budgets])
        }

    @property
    def handler(self):
        decision_handler = CallbackQueryHandler(self.decision, pass_user_data=True)

        return ConversationHandler(
            entry_points=[RegexHandler('\S*', self.home, pass_user_data=True)],

            states={
                HOME_DECISION: [decision_handler],
                ACCOUNT_DECISION: [decision_handler],
                FUNCTION_DECISION: [decision_handler]
            },

            fallbacks=[]
        )

    def home(self, bot, update, user_data):
        markup = self.create_markup(_BTS_MAIN)

        if update.callback_query is None:
            bot.send_message(update.message.chat_id, msg.HOME, reply_markup=markup)
        else:
            self.edit_message(bot, update, msg.HOME, markup)

        user_data[_STATE] = HOME_DECISION
        return HOME_DECISION

    def account(self, bot, update, user_data):
        markup = self.create_markup(_BTS_ACCOUNT, col=2)

        self.edit_message(bot, update, msg.ACCOUNT, markup)

        user_data[_STATE] = ACCOUNT_DECISION
        return ACCOUNT_DECISION

    def functions(self, bot, update, user_data):
        markup = self.create_markup(_BTS_FUNCTIONS, col=2, reverse=True)

        self.edit_message(bot, update, msg.FUNCTIONS, markup)

        user_data[_STATE] = FUNCTION_DECISION
        return FUNCTION_DECISION

    def decision(self, bot, update, user_data):
        choice = update.callback_query.data
        buttons, commands = self.bts_cmds[user_data[_STATE]]
        cmd = commands[buttons.index(choice)]

        return cmd(bot, update, user_data)

    def info(self, bot, update, user_data):
        pass

    def login(self, bot, update, user_data):
        pass

    def register(self, bot, update, user_data):
        pass

    def save_cents(self, bot, update, user_data):
        pass

    def budgets(self, bot, update, user_data):
        pass

    @staticmethod
    def edit_message(bot, update, text, markup):
        chat_id, msg_id = update.effective_message.chat_id, update.effective_message.message_id
        bot.edit_message_text(text=text, chat_id=chat_id, message_id=msg_id,
                              reply_markup=markup)
