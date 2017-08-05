import logging

from bunq.sdk.model.generated import MonetaryAccountBank, UserPerson, \
    object_

from api import api_context, get_active_accounts, get_iban, get_user

logger = logging.getLogger(__name__)


def setup_callbacks(savings_iban, url, category):
    user = get_user()
    accounts = get_active_accounts()
    accounts = [acc for acc in accounts if get_iban(acc) != savings_iban]

    for acc in accounts:
        res1 = _remove_callbacks(user, acc)
        res2 = _add_callback(user, acc, url, category)
        logger.info(f'Deleted all callbacks - Result {res1}. '
                    f'Added callback to account. Result - {res2}')


def _add_callback(user: UserPerson, account: MonetaryAccountBank, url,
                  category):
    callback_new = object_.NotificationFilter(
        "URL",
        url,
        category
    )
    request_map = {
        MonetaryAccountBank.FIELD_NOTIFICATION_FILTERS: [callback_new]
    }

    return MonetaryAccountBank.update(api_context(), request_map, user.id_,
                                      account.id_)


def _remove_callbacks(user: UserPerson, account: MonetaryAccountBank):
    callbacks_new = []
    request_map = {
        MonetaryAccountBank.FIELD_NOTIFICATION_FILTERS: callbacks_new
    }

    return MonetaryAccountBank.update(api_context(), request_map, user.id_,
                                      account.id_)
