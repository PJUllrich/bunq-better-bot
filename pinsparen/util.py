import logging
from typing import Union

from bunq.sdk.model import generated
from bunq.sdk.model.generated import MonetaryAccountBank

import api

logger = logging.getLogger(__name__)


def get_user():
    """
    Gets an UserPerson

    Returns
    -------
    generated.UserPerson
    """

    users = generated.User.list(api.Client.ctx())
    user_first: generated.UserPerson = users[0].UserPerson
    return user_first


def get_active_accounts():
    """
    Gets all the accounts that are active

    Returns
    -------
    generated.MonetaryAccountBank
    """

    user = get_user()
    accounts = get_all_accounts(user)
    return [acc for acc in accounts if acc.status == 'ACTIVE']


def get_all_accounts(user):
    """
    Gets all the accounts belonging to the user.

    Parameters
    ----------
    user    : generated.UserPerson

    Returns
    -------
    list[generated.UserPerson]
    """

    return MonetaryAccountBank.list(api.Client.ctx(), user.id_)


def get_iban(account):
    """
    Gets the iban of the account.

    Parameters
    ----------
    account    : generated.MonetaryAccountBank

    Returns
    -------
    None
        If no iban has been found.
    str
        If an iban has been found.
    """

    return get_attr_from_alias(account, 'value', 'IBAN')


def get_attr_from_alias(account, attr, alias_type):
    """
    Parameters
    ----------
    account     : MonetaryAccountBank
    attr        : str
    alias_type  : str

    Returns
    -------
    str
        If an iban has been found.
    """

    res = [getattr(a, attr) for a in account.alias if a.type_ == alias_type]
    if len(res) == 0 or res[0] is None:
        logger.error(f'Cannot get {attr} from type {alias_type} from account'
                     f'{account}')
        return None

    return res[0]


def get_account_for_iban(iban):
    """
    Parameters
    ----------
    iban    : str

    Returns
    -------
    MonetaryAccountBank
    """

    user = get_user()
    accounts = generated.MonetaryAccountBank.list(api.Client.ctx(), user.id_)
    for acc in accounts:
        for a in acc.alias:
            if a.type_ == 'IBAN' and a.value == iban:
                return acc


def make_payment(account_from, request_map):
    """
    Parameters
    ----------
    account_from    : MonetaryAccountBank
    request_map     : dict

    Returns
    -------
    dict
    """

    user = get_user()
    ctx = api.Client.ctx()

    payment_id = generated.Payment.create(ctx, request_map, user.id_,
                                          account_from.id_)

    res = generated.Payment.get(ctx, user.id_, account_from.id_, payment_id)
    res_json = res.to_json()

    return res_json
