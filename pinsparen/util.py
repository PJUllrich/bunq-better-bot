import logging

from bunq.sdk.model import generated
from bunq.sdk.model.generated import MonetaryAccountBank

import api

logger = logging.getLogger(__name__)


def get_user():
    users = generated.User.list(api.Client.ctx())
    user_first: generated.UserPerson = users[0].UserPerson
    return user_first


def get_active_accounts():
    user = get_user()
    accounts = get_all_accounts(user)
    return [acc for acc in accounts if acc.status == 'ACTIVE']


def get_all_accounts(user):
    return MonetaryAccountBank.list(api.Client.ctx(), user.id_)


def get_iban(account):
    return get_attr_from_alias(account, 'value', 'IBAN')


def get_attr_from_alias(account, attr, alias_type):
    res = [getattr(a, attr) for a in account.alias if a.type_ == alias_type]
    if len(res) == 0 or res[0] is None:
        logger.error(f'Cannot get {attr} from type {alias_type} from account'
                     f'{account}')
        return None

    return res[0]


def get_account_for_iban(iban):
    user = get_user()
    accounts = generated.MonetaryAccountBank.list(api.Client.ctx(), user.id_)
    for acc in accounts:
        for a in acc.alias:
            if a.type_ == 'IBAN' and a.value == iban:
                return acc


def make_payment(account_from: MonetaryAccountBank, request_map):
    user = get_user()
    ctx = api.Client.ctx()

    payment_id = generated.Payment.create(ctx, request_map, user.id_,
                                          account_from.id_)

    res = generated.Payment.get(ctx, user.id_, account_from.id_, payment_id)
    res_json = res.to_json()

    return res_json
