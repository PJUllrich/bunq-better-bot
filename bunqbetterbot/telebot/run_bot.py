import os

from telegrambot import TelegramBot
from util import logger

WEBHOOK_URL = os.environ['BUNQ_BOT_URL']
WEBHOOK_PATH = os.environ['BUNQ_BOT_URL_PATH']
BOT_TOKEN = os.environ['BUNQ_BOT_TOKEN']

WEBHOOK_PORT = 8525
LOG_FILENAME = 'better-bunq-bot.log'

if __name__ == "__main__":
    logger.setup_logger(LOG_FILENAME)

    bot = TelegramBot(BOT_TOKEN)
