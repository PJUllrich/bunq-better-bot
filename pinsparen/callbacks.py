import logging
from threading import Thread

from bunq.sdk.model.generated import MonetaryAccountBank, UserPerson
from bunq.sdk.model.generated.object_ import NotificationFilter

import api
import util

logger = logging.getLogger(__name__)


class Callback:
    def __init__(self, category, url):
        """
        Parameters
        ----------
        category    : str
            The catagory of the callback in all caps. Catagories can be found
            here: https://doc.bunq.com/api/1/page/callbacks
        url         : str
            The target url for the POST callback notification.
        """

        self.category = category
        self.url = url


def setup_callbacks(accounts, callbacks):
    """
    Parameters
    ----------
    accounts    : list[MonetaryAccountBank]
    callbacks   : list[Callback]
    """

    user = util.get_user()

    for acc in accounts:
        t = Thread(target=reset_and_add_callbacks, args=(user, acc, callbacks))
        t.start()


def reset_and_add_callbacks(user, account, callbacks):
    """
    Parameters
    ----------
    user        : UserPerson
    account     : MonetaryAccountBank
    callbacks   : list[Callback]
    """

    res1 = _remove_callbacks(user, account)
    res2 = _add_callbacks(user, account, callbacks)
    logger.info(f'Deleted all callbacks - Result {res1}. '
                f'Added callbacks to account. Result - {res2}')


def _add_callbacks(user, account, callbacks):
    """
    Parameters
    ----------
    user        : UserPerson
    account     : MonetaryAccountBank
    callbacks   : list[Callback]

    Returns
    -------
    MonetaryAccountBank
    """

    callbacks_new = [NotificationFilter('URL', c.url, c.category) for c in
                     callbacks]
    request_map = {
        MonetaryAccountBank.FIELD_NOTIFICATION_FILTERS: callbacks_new
    }

    return MonetaryAccountBank.update(api.Client.ctx(), request_map, user.id_,
                                      account.id_)


def _remove_callbacks(user, account):
    """

    Parameters
    ----------
    user    : UserPerson
    account : MonetaryAccountBank

    Returns
    -------
    MonetaryAccountBank
    """

    return _add_callbacks(user, account, [])
