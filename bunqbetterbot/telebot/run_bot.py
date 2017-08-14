from telegrambot import TelegramBot
from util import logger

LOG_FILENAME = 'bunqBetterBot-bot.log'

if __name__ == "__main__":
    logger.setup_logger(LOG_FILENAME)

    bot = TelegramBot()
