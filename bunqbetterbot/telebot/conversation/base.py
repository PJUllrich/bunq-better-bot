from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from util.const import USER_STATE


class Base:
    btn_cmd_map = {}

    @classmethod
    def create_markup(cls, data, col=1, reverse=False):
        keys = []
        for r in range(0, len(data), col):
            keys.append([cls.get_button(data[c]) for c in range(r, min(r + col, len(data)))])

        if reverse:
            keys.reverse()

        return InlineKeyboardMarkup(keys)

    @staticmethod
    def get_button(data):
        return InlineKeyboardButton(str(data), callback_data=str(data))

    @classmethod
    def decision(cls, bot, update, user_data):
        choice = update.callback_query.data
        buttons, commands = cls.btn_cmd_map[user_data[USER_STATE]]
        try:
            cmd_idx = buttons.index(choice)
            cmd = commands[cmd_idx]
            return cmd(bot, update, user_data)
        except ValueError:
            return False

    @staticmethod
    def edit_message(bot, update, text, markup, parse_mode=ParseMode.MARKDOWN):
        chat_id = update.effective_message.chat_id
        msg_id = update.effective_message.message_id

        bot.edit_message_text(text=text, reply_markup=markup,
                              chat_id=chat_id, message_id=msg_id,
                              parse_mode=parse_mode)

    @staticmethod
    def send_typing(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
