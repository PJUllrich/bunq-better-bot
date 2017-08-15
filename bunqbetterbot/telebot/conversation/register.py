import base64
import logging

from telegram import ParseMode

import conversation
import msg.general
import msg.register
from conversation import main
from conversation.base import USER_STATE
from logic.interface import BotInterface
from util import security

logger = logging.getLogger(__name__)

BTS_ENV = ['Sandbox', 'Production']


class Register(conversation.Base):
    @classmethod
    def start(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_ENV, col=2)
        cls.edit_message(bot, update, msg.register.START + msg.register.ENV, markup=markup)

        return main.REGISTER_ENV

    @classmethod
    def environment(cls, bot, update, user_data):
        env = update.callback_query.data
        user_data['env'] = env.upper()

        cls.edit_message(bot, update, msg.register.KEY, markup=[])

        return main.REGISTER_KEY

    @classmethod
    def api_key(cls, bot, update, user_data):
        key = update.message.text
        user_data['key_api'] = key

        bot.send_message(update.message.chat_id, msg.register.PASS, parse_mode=ParseMode.MARKDOWN)

        return main.REGISTER_PW

    @classmethod
    def password(cls, bot, update, user_data):
        cls.set_authentication_params(update, user_data)

        res = BotInterface.register(user_data)

        user_data.clear()

        if res.status_code != 201:
            ans = msg.general.ERROR
            logger.error(f'Error occurred during registration: {res.content.decode()}')
        else:
            ans = msg.register.END

        markup = cls.create_markup(main.BTS_ACCOUNT, col=2)
        bot.send_message(update.message.chat_id, ans, reply_markup=markup)

        user_data[USER_STATE] = main.ACCOUNT_DECISION
        return main.ACCOUNT_DECISION

    @classmethod
    def set_authentication_params(cls, update, user_data):
        password_clear = update.message.text
        password_hashed = security.hash_key(password_clear)

        del password_clear
        del update.message.text

        user_data['chat_id'] = update.message.chat_id
        user_data['pw'] = password_hashed

    @classmethod
    def _bytes_to_str(cls, data):
        return base64.b64encode(data).decode()
