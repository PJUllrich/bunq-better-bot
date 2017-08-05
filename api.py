import logging
from json import JSONDecodeError

from bunq.sdk import context
from bunq.sdk.model import generated
from bunq.sdk.model.generated import UserPerson

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
    user_first: UserPerson = users[0].UserPerson
    return user_first


def get_account_for_iban(iban):
    user = get_user()
    accounts = generated.MonetaryAccountBank.list(api_context(), user.id_)
    for acc in accounts:
        for a in acc.alias:
            if a.type_ == 'IBAN' and a.value == iban:
                return acc
