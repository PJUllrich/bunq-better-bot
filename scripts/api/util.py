import logging
import time
from datetime import datetime, timezone

from bunq.sdk.model import generated
from bunq.sdk.model.generated import MonetaryAccountBank, Payment

from api.client import Client

logger = logging.getLogger(__name__)

_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def get_user():
    """
    Gets an UserPerson

    Returns
    -------
    generated.UserPerson
    """

    users = generated.User.list(Client.ctx())
    user_first: generated.UserPerson = users[0].UserPerson
    return user_first


def get_active_accounts():
    """
    Gets all the accounts that are active

    Returns
    -------
    list[generated.MonetaryAccountBank]
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
    list[generated.MonetaryAccountBank]
    """

    return MonetaryAccountBank.list(Client.ctx(), user.id_)


def get_iban(account):
    """
    Gets the iban of the account.

    Parameters
    ----------
    account    : generated.MonetaryAccountBank

    Returns
    -------
    str
        If an iban has been found. None otherwise
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
    accounts = generated.MonetaryAccountBank.list(Client.ctx(), user.id_)
    for acc in accounts:
        for a in acc.alias:
            if a.type_ == 'IBAN' and a.value == iban:
                return acc


def make_payment(account_from, request_map):
    """
    Creates a new Payment object with a given request_map and an account from
    which the Payment should be made

    Parameters
    ----------
    account_from    : MonetaryAccountBank, the account from which to make the
                        Payment
    request_map     : dict

    Returns
    -------
    dict            : Response from bunq API
    """

    user = get_user()
    ctx = Client.ctx()

    payment_id = generated.Payment.create(ctx, request_map, user.id_,
                                          account_from.id_)

    res = generated.Payment.get(ctx, user.id_, account_from.id_, payment_id)
    res_json = res.to_json()

    return res_json


def get_datetime(from_str):
    """
    Converts a string input to a datetime object using the _DATETIME_FORMAT
    format.

    Parameters
    ----------
    from_str    : str, string representation of a datetime object

    Returns
    -------
    datetime    : datetime object with same date and time as input string
    """

    since_epoch = time.mktime(time.strptime(from_str, _DATETIME_FORMAT))
    return datetime.fromtimestamp(since_epoch, tz=timezone.utc)


def get_transactions_for_date_range(account, start_date, end_date=None):
    """
    Gets the transactions of an account from a specific start date until a
    given end date.

    Parameters
    ----------
    account     : MonetaryAccountBank, the account for which to get the
                    transactions
    start_date  : datetime object
    end_date    : datetime object, when None will use current datetime

    Returns
    -------
    list[Payment]
    """

    if end_date is None:
        end_date = datetime.now(timezone.utc)

    if end_date < start_date:
        raise ValueError('End date cannot be before start date.')

    user = get_user()
    transactions = Payment.list(Client.ctx(), user.id_, account.id_)
    transactions_in_range = [t for t in transactions if
                             start_date <= get_datetime(t.created) <= end_date]

    return transactions_in_range
