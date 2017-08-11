import os

import util.logger as logger
from telebot.telegrambot import TelegramBot
from func.interface import Interface

_BOT_TOKEN = os.environ['BUNQ_BOT_TOKEN']
_LOG_FILENAME = 'better-bunq-bot.log'

if __name__ == "__main__":
    logger.setup_logger(_LOG_FILENAME)

    func_interface = Interface()
    bot = TelegramBot(_BOT_TOKEN, func_interface)
