from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STATE = 'STATE'


class Base:
    btn_cmd_map = { }
    actions = None

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
        buttons, commands = cls.btn_cmd_map[user_data[STATE]]
        cmd = commands[buttons.index(choice)]

        return cmd(bot, update, user_data)

    @staticmethod
    def edit_message(bot, update, text, markup):
        chat_id, msg_id = update.effective_message.chat_id, update.effective_message.message_id
        bot.edit_message_text(text=text, chat_id=chat_id, message_id=msg_id,
                              reply_markup=markup)
