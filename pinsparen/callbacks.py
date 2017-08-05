import logging

from bunq.sdk.model.generated import MonetaryAccountBank, UserPerson, \
    object_

import api

logger = logging.getLogger(__name__)


def setup_callbacks(url, category):
    user = api.get_user()
    accounts = _get_all_accounts(user)

    for acc in accounts:
        res = _add_callback(user, acc, url, category)
        logger.info(f'Added callback to account. Result - {res}')


def reset_callbacks():
    user = api.get_user()
    accounts = _get_all_accounts(user)

    for acc in accounts:
        _remove_callbacks(user, acc)


def _get_all_accounts(user):
    return MonetaryAccountBank.list(api.api_context(), user.id_)


def _add_callback(user: UserPerson, account: MonetaryAccountBank, url,
                  category):
    callbacks_old = account.notification_filters
    callback_to_add = object_.NotificationFilter(
        "URL",
        url,
        category
    )
    callbacks_old.append(callback_to_add)
    request_map = {
        MonetaryAccountBank.FIELD_NOTIFICATION_FILTERS: callbacks_old
    }

    return MonetaryAccountBank.update(api.api_context(), request_map, user.id_,
                                      account.id_)


def _remove_callbacks(user: UserPerson, account: MonetaryAccountBank):
    callbacks_new = []
    request_map = {
        MonetaryAccountBank.FIELD_NOTIFICATION_FILTERS: callbacks_new
    }

    return MonetaryAccountBank.update(api.api_context(), request_map, user.id_,
                                      account.id_)
