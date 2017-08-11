import inspect
import json

from telebot import msg


def owner_only(func):
    def inner(self, bot, update):
        if self.chat_id is not None and self.chat_id != update.message.chat_id:
            bot.send_message(update.message.chat_id, msg.NO_PERMISSION)
        else:
            return func(self, bot, update)

    return inner


def decode_json(func):
    def inner(data_json):
        data_dict = json.loads(data_json)
        return func(data_dict)

    return inner


def decode_dict(func):
    params = inspect.getargspec(func)[0]

    def inner(data):
        args = [data.get(p) for p in params]

        if None in args:
            raise ValueError('Not all necessary data was passed.')

        return func(*args)

    return inner
