import util.security as security

from telebot import msg
from telebot.conversation import main
from telebot.conversation.base import Base


class Login(Base):
    @classmethod
    def start(cls, bot, update, user_data):
        # TODO: Check whether user is registered
        cls.edit_message(bot, update, msg.LOGIN_START, [])

        return main.LOGIN_PW

    @classmethod
    def password(cls, bot, update, user_data):
        pw_hashed = security.hash_password(update.message.text)
        del update.message.text

        data = {
            'chat_id': update.message.chat_id,
            'pw_hashed': pw_hashed
        }

        authenticated = cls.actions.login(data)

        if not authenticated:
            bot.send_message(update.message.chat_id, msg.LOGIN_FAIL)
            return main.LOGIN_PW

        ans = msg.DELETE_MSG.format('password')
        markup = cls.create_markup(main.BTS_DELETE_MSG)
        bot.send_message(update.message.chat_id, ans, reply_markup=markup)

        return main.LOGIN_DEL
