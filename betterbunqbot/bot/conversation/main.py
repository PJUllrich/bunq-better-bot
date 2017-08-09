import random

from telegram.ext import CallbackQueryHandler, ConversationHandler, RegexHandler

from bot import msg
from bot.conversation.base import BaseConversation

HOME, ACCOUNT, FUNCTIONS = range(3)

_BTS_MAIN = ['Account', 'Functions']


class MainConversation(BaseConversation):
    def __init__(self):
        self.fresh = True

    @property
    def handler(self):
        return ConversationHandler(
            entry_points=[RegexHandler('\S*', self.home)],

            states={
                HOME: [CallbackQueryHandler(self.home)]
            },

            fallbacks=[]
        )

    def home(self, bot, update):
        markup = self._get_markup_main()

        if not self.fresh:
            chat_id = update.effective_message.chat_id
            msg_id = update.effective_message.message_id
            ans = f'Test - {random.randint(1, 100)}'
            bot.edit_message_text(text=ans, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        else:
            res = bot.send_message(update.message.chat_id, msg.HOME, reply_markup=markup)
            self.fresh = False

        return HOME

    def _get_markup_main(self):
        return self.create_markup(_BTS_MAIN)
