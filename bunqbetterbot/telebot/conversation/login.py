import json

from telegram import ParseMode

import conversation
import msg.general
import msg.login
from conversation import main
from conversation.base import USER_STATE
from logic.interface import BotInterface
from util import const, security


class Login(conversation.Base):
    @classmethod
    def start(cls, bot, update, user_data):
        # TODO: Check whether user is registered

        user_data['login_attempt'] = 1
        cls.edit_message(bot, update, msg.login.START, [])

        return main.LOGIN_PW

    @classmethod
    def password(cls, bot, update, user_data):
        message = update.message if update.message is not None else update.edited_message

        data = cls._get_login_data(message)
        authenticated = BotInterface.login(data)

        if authenticated.status_code != 200:
            return cls._handle_login_fail(bot, message, user_data)

        return cls._handle_login_success(bot, message, authenticated, user_data)

    @classmethod
    def delete(cls, bot, update, user_data):
        markup = cls.create_markup(main.BTS_MAIN)
        cls.edit_message(bot, update, msg.login.END, markup)

        user_data[USER_STATE] = main.HOME_DECISION
        return main.HOME_DECISION

    @classmethod
    def _get_login_data(cls, message):
        pw_hashed = security.hash_key(message.text)

        return {
            'chat_id': message.chat_id,
            'pw': pw_hashed
        }

    @classmethod
    def _handle_login_fail(cls, bot, message, user_data):
        ans = f"Attempt Nr.: {user_data['login_attempt']}\n\n" + msg.login.FAIL
        bot.send_message(message.chat_id, ans)

        user_data['login_attempt'] += 1
        return main.LOGIN_PW

    @classmethod
    def _handle_login_success(cls, bot, message, authenticated, user_data):
        content = json.loads(authenticated.content.decode())

        user_data[const.AUTH_TOKEN] = content[const.AUTH_TOKEN]
        ans = msg.general.DELETE_MSG.format('password')
        markup = cls.create_markup(main.BTS_DELETE_MSG, col=2)
        bot.send_message(message.chat_id, ans, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

        return main.LOGIN_DEL
