import logging

from bunq.sdk.model import generated
from bunq.sdk.model.generated import MonetaryAccountBank, object_

import api

logger = logging.getLogger(__name__)

__SAVINGS_ACCOUNT: MonetaryAccountBank = None
__SAVING_PAYMENT_DESCRIPTION = 'Saving cents through pinsparen.py'


def set_savings_account(savings_iban):
    """Sets up the account to which the saved cents should be sent.
    Needs to be run before any other method from this script!
    """
    global __SAVINGS_ACCOUNT
    __SAVINGS_ACCOUNT = api.get_account_for_iban(savings_iban)


def round_account_balances(msg_json):
    category = msg_json['NotificationUrl']['category']
    logger.info(f'Received Callback - {category}')

    user = api.get_user()
    accounts = generated.MonetaryAccountBank.list(api.api_context(), user.id_)
    savings_iban = _get_iban(__SAVINGS_ACCOUNT)
    for acc in accounts:
        if _get_iban(acc) != savings_iban:
            _round_balance(acc)


def _round_balance(account):
    amount_to_save = _get_amount_to_save(account)
    if amount_to_save > 0:
        make_payment(account, __SAVINGS_ACCOUNT, amount_to_save)
    else:
        logger.info('Amount to save was 0. Doing nothing.')


def _get_amount_to_save(account):
    amount_to_save = round(float(account.balance.value) % 0.50, 2)
    return amount_to_save


def make_payment(account_from, account_to, amount):
    iban_to = _get_iban(account_to)
    request_map = {
        generated.Payment.FIELD_AMOUNT: object_.Amount(
            abs(amount),
            'EUR'
        ),
        generated.Payment.FIELD_COUNTERPARTY_ALIAS: object_.Pointer(
            'IBAN',
            iban_to
        ),
        generated.Payment.FIELD_DESCRIPTION: __SAVING_PAYMENT_DESCRIPTION,
    }

    request_map[generated.Payment.FIELD_COUNTERPARTY_ALIAS].name = \
        _get_alias_name(account_to)

    user = api.get_user()
    ctx = api.api_context()

    payment_id = generated.Payment.create(ctx,
                                          request_map,
                                          user.id_,
                                          account_from.id_)

    generated.Payment.get(ctx, user.id_, account_from.id_, payment_id).to_json()

    iban_from = _get_iban(account_from)
    logger.info(f'Transferred {amount} Euro from {iban_from} to {iban_to}')


def _get_iban(account):
    return [a.value for a in account.alias if a.type_ == 'IBAN'][0]


def _get_alias_name(account):
    return [a.name for a in account.alias if a.type_ == 'IBAN'][0]
