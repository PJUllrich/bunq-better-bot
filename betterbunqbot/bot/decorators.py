from bot import msg


def owner_only(func):
    def inner(self, bot, update):
        if self.chat_id is not None and self.chat_id != update.message.chat_id:
            bot.send_message(update.message.chat_id, msg.NO_PERMISSION)
        else:
            return func(self, bot, update)

    return inner
