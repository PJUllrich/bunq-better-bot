import logging
from json import JSONDecodeError

from bunq.sdk import context

logger = logging.getLogger(__name__)


class Client:
    @classmethod
    def setup_api_context(cls, environment, api_key, description):
        try:
            return context.ApiContext.restore()
        except (FileNotFoundError, JSONDecodeError):
            ctx = context.ApiContext(environment, api_key, description)
            ctx.save()

    @classmethod
    def ctx(cls):
        try:
            return context.ApiContext.restore()
        except (FileNotFoundError, JSONDecodeError):
            logger.critical(
                'ApiContext not yet set. Set it up before using it.')
