from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class BaseConversation:
    @staticmethod
    def create_markup(data, col=1):
        keys = []
        for r in range(0, len(data), col):
            keys.append([BaseConversation.get_button(data[c]) for c in range(r, r + col)])

        return InlineKeyboardMarkup(keys)

    @staticmethod
    def get_button(data):
        return InlineKeyboardButton(str(data), callback_data=str(data))
