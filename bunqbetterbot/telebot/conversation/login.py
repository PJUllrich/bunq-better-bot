from telegram import ParseMode

import conversation
import msg.general
import msg.login
from conversation import main
from conversation.base import USER_STATE
from logic.interface import BotInterface
from util import security


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
        pw_hashed = security.hash_key(message.text)

        data = {
            'chat_id': message.chat_id,
            'pw': pw_hashed
        }

        authenticated = BotInterface.login(data)

        if not authenticated:
            return cls._handle_login_fail(bot, update, user_data)

        ans = msg.general.DELETE_MSG.format('password')
        markup = cls.create_markup(main.BTS_DELETE_MSG, col=2)
        bot.send_message(message.chat_id, ans, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

        return main.LOGIN_DEL

    @classmethod
    def delete(cls, bot, update, user_data):
        markup = cls.create_markup(main.BTS_MAIN)
        cls.edit_message(bot, update, msg.login.END, markup)

        user_data[USER_STATE] = main.HOME_DECISION
        return main.HOME_DECISION

    @classmethod
    def _handle_login_fail(cls, bot, update, user_data):
        ans = f"Attempt Nr.: {user_data['login_attempt']}\n\n" + msg.login.FAIL
        bot.send_message(update.message.chat_id, ans)

        user_data['login_attempt'] += 1
        return main.LOGIN_PW
