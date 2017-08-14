from datetime import timedelta

import os

from util import security


class DevConfig:
    SECRET_KEY = os.urandom(security.KEY_LENGTH)
    SESSION_TYPE = 'memcached'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
