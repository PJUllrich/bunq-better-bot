import logging
from json import JSONDecodeError

from bunq.sdk import context
from bunq.sdk.model import generated
from bunq.sdk.model.generated import MonetaryAccountBank

logger = logging.getLogger(__name__)


def setup_api_context(environment, api_key, description):
    try:
        return context.ApiContext.restore()
    except (FileNotFoundError, JSONDecodeError):
        ctx = context.ApiContext(environment, api_key, description)
        ctx.save()


def api_context():
    try:
        return context.ApiContext.restore()
    except (FileNotFoundError, JSONDecodeError):
        logger.critical('ApiContext not yet set. Set it up before using it.')


def get_user():
    users = generated.User.list(api_context())
    user_first: generated.UserPerson = users[0].UserPerson
    return user_first


def get_active_accounts():
    user = get_user()
    accounts = _get_all_accounts(user)
    return [acc for acc in accounts if acc.status == 'ACTIVE']


def _get_all_accounts(user):
    return MonetaryAccountBank.list(api_context(), user.id_)


def get_iban(account):
    return get_attr_from_alias(account, 'value', 'IBAN')


def get_attr_from_alias(account, attr, alias_type):
    res = [getattr(a, attr) for a in account.alias if a.type_ == alias_type]
    if len(res) == 0 or res[0] is None:
        logger.error(f'Cannot get {attr} from type {alias_type} from account' \
                     f'{account}')
        return None

    return res[0]


def get_account_for_iban(iban):
    user = get_user()
    accounts = generated.MonetaryAccountBank.list(api_context(), user.id_)
    for acc in accounts:
        for a in acc.alias:
            if a.type_ == 'IBAN' and a.value == iban:
                return acc
