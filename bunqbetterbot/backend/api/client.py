import logging
from json import JSONDecodeError

from bunq.sdk import context

logger = logging.getLogger(__name__)


class Client:
    @classmethod
    def setup_api_context(cls, environment, api_key, description):
        """
        Parameters
        ----------
        environment : context.ApiEnvironmentType
        api_key     : str
            The api key you got from the bunq flask-app.
        description : str
            Description of the device you are connecting the the bunq api.

        Returns
        -------
        context.ApiContext
        """

        try:
            return context.ApiContext.restore()
        except (FileNotFoundError, JSONDecodeError):
            ctx = context.ApiContext(environment, api_key, description)
            ctx.save()

    @classmethod
    def ctx(cls):
        """
        Returns
        -------
        context.ApiContext
            The ApiContext if its setup correctly.
        """

        try:
            return context.ApiContext.restore()
        except (FileNotFoundError, JSONDecodeError):
            logger.critical(
                'ApiContext not yet set. Set it up before using it.')
