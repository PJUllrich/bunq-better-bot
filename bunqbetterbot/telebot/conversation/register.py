import json

import base64

import util.security as security
from telebot import msg
from telebot.conversation import main
from telebot.conversation.base import Base

BTS_ENV = ['Sandbox', 'Production']


class Register(Base):
    @classmethod
    def start(cls, bot, update, user_data):
        markup = cls.create_markup(BTS_ENV, col=2)
        cls.edit_message(bot, update, msg.REGISTER_START + msg.REGISTER_ENV, markup=markup)

        return main.REGISTER_ENV

    @classmethod
    def environment(cls, bot, update, user_data):
        env = update.callback_query.data
        user_data['env'] = env.upper()

        cls.edit_message(bot, update, msg.REGISTER_KEY, markup=[])

        return main.REGISTER_KEY

    @classmethod
    def api_key(cls, bot, update, user_data):
        key = update.message.text
        user_data['key_api'] = key

        bot.send_message(update.message.chat_id, msg.REGISTER_PASS)

        return main.REGISTER_PW

    @classmethod
    def password(cls, bot, update, user_data):
        cls.set_authentication_params(update, user_data)

        cls.actions.register(json.dumps(user_data))

        markup = cls.create_markup(main.BTS_ACCOUNT, col=2)
        bot.send_message(update.message.chat_id, msg.REGISTER_END, reply_markup=markup)

        return main.ACCOUNT_DECISION

    @classmethod
    def set_authentication_params(cls, update, user_data):
        password_clear = update.message.text
        del update.message.text

        password_derivated = security.derivate_key(password_clear.encode())
        password_hash = security.hash_key(password_derivated).hexdigest()

        encrypt_key, encrypt_iv = security.encrypt(security.create_random_key(), password_derivated)
        api_key, api_iv = security.encrypt(user_data['key_api'].encode(), encrypt_key)

        del password_derivated
        del user_data['key_api']

        user_data['chat_id'] = update.message.chat_id
        user_data['password_hash'] = password_hash
        user_data['key_api'] = {'key': cls._bytes_to_str(api_key),
                                'iv': cls._bytes_to_str(api_iv)}
        user_data['key_encrypt'] = {'key': cls._bytes_to_str(encrypt_key),
                                    'iv': cls._bytes_to_str(encrypt_iv)}

    @classmethod
    def _bytes_to_str(cls, data):
        return base64.b64encode(data).decode()
