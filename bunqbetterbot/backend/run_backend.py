from flask import Flask

import app.config
from util import logger

backend = Flask(__name__)

# Change this once moving from development to production
backend.config.from_object(app.config.DevConfig)

# This is needed in order to load the routes
from app.routes import *

LOG_FILENAME = 'bunqBetterBot-backend.log'

if __name__ == '__main__':
    logger.setup_logger(LOG_FILENAME)

    backend.run()
