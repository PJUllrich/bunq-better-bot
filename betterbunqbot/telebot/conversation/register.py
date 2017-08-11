import json

import base64
from telegram.ext import CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

import util.security as security
from telebot import msg
from telebot.conversation.base import BaseConversation

API_KEY, PASSWORD = range(2)

_BTS_ENV = ['Sandbox', 'Production']


class RegisterConversation(BaseConversation):
    @property
    def handler(self):
        return ConversationHandler(
            entry_points=[CallbackQueryHandler(self.environment, pass_user_data=True)],

            states={
                API_KEY: [MessageHandler(Filters.text, self.api_key, pass_user_data=True)],
                PASSWORD: [MessageHandler(Filters.text, self.password, pass_user_data=True)]
            },

            fallbacks=[]
        )

    @classmethod
    def environment(cls, bot, update, user_data):
        env = update.callback_query.data
        user_data['env'] = env.upper()

        cls.edit_message(bot, update, msg.REGISTER_KEY, markup=[])

        return API_KEY

    @classmethod
    def api_key(cls, bot, update, user_data):
        key = update.message.text
        user_data['key_api'] = key

        bot.send_message(update.message.chat_id, msg.REGISTER_PASS)

        return PASSWORD

    @classmethod
    def password(cls, bot, update, user_data):
        cls.set_authentication_params(update, user_data)

        cls.actions.register(json.dumps(user_data))

        bot.send_message(update.message.chat_id, msg.REGISTER_END, reply_markup=[])

        return -2

    @classmethod
    def set_authentication_params(cls, update, user_data):
        password_clear = update.message.text
        password_derivated = security.derivate_key(password_clear.encode())
        password_hash = security.hash_key(password_derivated).hexdigest()

        encrypt = cls._create_key_encrypted(security.create_random_key(), password_derivated)
        api = cls._create_key_encrypted(user_data['key_api'].encode(), encrypt.key_encypted_bytes)

        del password_clear
        del password_derivated
        del user_data['key_api']

        user_data['chat_id'] = update.message.chat_id
        user_data['password_hash'] = password_hash
        user_data['key_api'] = json.dumps(api.__dict__)
        user_data['key_encrypt'] = json.dumps(encrypt.__dict__)

    @classmethod
    def _create_key_encrypted(cls, key, password):
        key_encrypted_bytes, iv_bytes = security.encrypt(key, password)

        key_encrypted_str = base64.b64encode(key_encrypted_bytes).decode()
        iv_str = base64.b64encode(iv_bytes).decode()

        return security.KeyEncrypted(key_encrypted_str, iv_str)
