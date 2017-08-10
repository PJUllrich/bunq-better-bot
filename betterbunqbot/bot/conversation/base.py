from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class BaseConversation:
    @classmethod
    def create_markup(cls, data, col=1, reverse=False):
        keys = []
        for r in range(0, len(data), col):
            keys.append([cls.get_button(data[c]) for c in range(r, min(r + col, len(data)))])

        keys.reverse() if reverse

        return InlineKeyboardMarkup(keys)

    @staticmethod
    def get_button(data):
        return InlineKeyboardButton(str(data), callback_data=str(data))
