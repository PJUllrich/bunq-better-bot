import logging

from bunq.sdk.model import generated
from bunq.sdk.model.generated import object_

import api.util as util
from func.save.handler.basehandler import BaseHandler

logger = logging.getLogger(__name__)


class BalanceRoundingHandler(BaseHandler):
    _SAVING_PAYMENT_DESCRIPTION = 'Saving cents through pinsparen.py'
    _ROUNDING_FACTOR = 0.50

    def __init__(self, savings_IBAN):
        self.savings_account = util.get_account_for_iban(savings_IBAN)
        if self.savings_account is None:
            logger.fatal(f'Could not find Savings Account with IBAN - '
                         f'{savings_IBAN}')
            exit(-1)

    def handle_event(self, msg_json):
        """
        Mandatory to implement.

        Can be called from EventHandler with JSON data.

        Parameters
        ----------
        msg_json    : dict, HTTP request body from Callback

        """
        self.round_account_balances(msg_json)

    def round_account_balances(self, msg_json):
        """
        Iterates through all active accounts, except the savings account
        and rounds the account's balance down to either x.00 or x.50, depending
        on the _ROUNDING_FACTOR

        Parameters
        ----------
        msg_json    : dict, HTTP request body from Callback

        """
        category = msg_json['NotificationUrl']['category']
        logger.info(f'Received Callback - {category}')

        accounts = util.get_active_accounts()
        savings_IBAN = util.get_iban(self.savings_account)
        for acc in accounts:
            if util.get_iban(acc) != savings_IBAN:
                self._round_balance(acc)

    def _round_balance(self, account):
        # TODO: Check the result from make_payment for success
        """Calculates the amount that needs to be transferred to the savings
        account in order to round the account's balance to either x.00 or
        x.50, depending on the _ROUNDING_FACTOR

        Creates a request map with data to which account which amount should
        be transferred.

        Sends this request map to the make_payment function and logs the result

        """
        amount_to_save = self._get_amount_to_save(account)
        if amount_to_save > 0:
            request_map = self._create_payment_request_map(self.savings_account,
                                                           amount_to_save)
            res = util.make_payment(account, request_map)
            logger.debug(f'Payment made. Response: {res}')

            IBAN_from = util.get_iban(account)
            logger.info(f'Transferred {amount_to_save:.2f} Euro from '
                        f'{IBAN_from} to {util.get_iban(self.savings_account)}')
        else:
            logger.info('Amount to save was 0.00. Doing nothing.')

    def _get_amount_to_save(self, account):
        """Takes the modulo of an account's balance and the _ROUNDING_FACTOR.
        Rounds that amount to 2 floating points.
        """
        amount_precise = float(account.balance.value) % self._ROUNDING_FACTOR
        amount_rounded = round(amount_precise, 2)
        return amount_rounded

    def _create_payment_request_map(self, account_to, amount):
        """Creates a request map for an IBAN -> IBAN transaction with a
        given (absolute) amount (in EUR)
        """
        request_map = {
            generated.Payment.FIELD_AMOUNT: object_.Amount(
                abs(amount),
                'EUR'
            ),
            generated.Payment.FIELD_COUNTERPARTY_ALIAS: object_.Pointer(
                'IBAN',
                util.get_iban(account_to)
            ),
            generated.Payment.FIELD_DESCRIPTION:
                self._SAVING_PAYMENT_DESCRIPTION,
        }

        request_map[generated.Payment.FIELD_COUNTERPARTY_ALIAS].name = \
            util.get_attr_from_alias(account_to, 'name', 'IBAN')

        return request_map
