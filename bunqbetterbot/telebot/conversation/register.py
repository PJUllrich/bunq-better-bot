import base64

import conversation
import msg.register
from conversation import main
from logic.interface import BotInterface
from util import security

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

        bot.send_message(update.message.chat_id, msg.register.PASS)

        return main.REGISTER_PW

    @classmethod
    def password(cls, bot, update, user_data):
        cls.set_authentication_params(update, user_data)

        res = BotInterface.register(user_data)

        markup = cls.create_markup(main.BTS_ACCOUNT, col=2)
        bot.send_message(update.message.chat_id, msg.register.END, reply_markup=markup)

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
