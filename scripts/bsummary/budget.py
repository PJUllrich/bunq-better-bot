from datetime import datetime, timedelta, timezone

from api.util import get_iban, get_transactions_for_date_range
from util.dtime import get_early_midnight, get_late_midnight


class Budget:
    _DEFAULT_DAYS_COVERED = 1

    def __init__(self, name, IBANs, keywords=None):
        self.name = name
        self.IBANs = IBANs
        self.keywords = keywords
        self.days_covered = self._DEFAULT_DAYS_COVERED

    def calc_budget(self, accounts_all):
        """
        Calculates the total amount of the outgoing expenses (except for
        payments to own accounts) in a specified time range
        (Default: for the last day)

        Parameters
        ----------
        accounts_all    : list[MonetaryAccountBank], all accounts of a user

        Returns
        -------
        float           : sum of all outgoing payment values
        """

        accounts_used = self._get_budget_accounts(accounts_all)

        payments_all = [self._get_payments(acc) for acc in accounts_used]
        payments_out = [self._get_outgoing(p) for p in payments_all]
        payments_for = [self._get_to_foreign(p, accounts_all)
                        for p in payments_out]

        expense = self._get_total_expense(payments_for)

        return expense

    def _get_budget_accounts(self, accounts):
        """
        Iterates through a list of MonetaryAccountBank objects and selects
        those whose IBAN matches an IBAN in self.IBANs

        Parameters
        ----------
        accounts    : list[MonetaryAccountBank], all accounts of a user

        Returns
        -------
        list[MonetaryAccountBank]   : All accounts whose IBAN is in self.IBANs
        """

        return [acc for acc in accounts if get_iban(acc) in self.IBANs]

    def _get_payments(self, account):
        """
        Gets all payments for a given account for the date range returned
        from self._get_date_range

        Parameters
        ----------
        account         : MonetaryAccountBank, for which to get the payments

        Returns
        -------
        list[Payment]   : all Payments for an account for a given date range
        """

        start, end = self._get_date_range()
        payments_all = get_transactions_for_date_range(account, start, end)
        return payments_all

    @staticmethod
    def _get_outgoing(payments):
        """
        Selects payments that are from the GIVEN account to ANOTHER account and
        therefore filters out payments that are incoming (i.e. from ANOTHER
        account to the GIVEN account)

        Parameters
        ----------
        payments        : list[Payment]

        Returns
        -------
        list[Payment]   : all Payments from the GIVEN account to ANOTHER account
        """

        payments_out = [p for p in payments if float(p.amount.value) < 0]

        return payments_out

    def _get_date_range(self):
        """
        Creates 2 datetime objects, one being at the earliest possible time
        (00:00:00.1) of the date self.days_covered days before today and one
        being today minus one day at late midnight (23:59:59.999999)

        Returns
        -------
        (datetime, datetime)    : start and end of a date range
        """

        now = datetime.now(timezone.utc)

        date_start = get_early_midnight(now - timedelta(days=self.days_covered))
        date_end = get_late_midnight(now - timedelta(days=1))

        return date_start, date_end

    def _get_to_foreign(self, payments, accounts_own):
        """
        Selects payments that were done to accounts that are not among the
        own accounts, thus payments going to 'foreign' accounts.

        Parameters
        ----------
        payments        : list[Payment]
        accounts_own    : list[MonetaryAccountBank]

        Returns
        -------
        list[Payment]   : the filtered list of payments
        """

        IBANs_own = [get_iban(acc) for acc in accounts_own]
        payments_filtered = [p for p in payments if
                             self._is_to_foreign(p, IBANs_own)]
        return payments_filtered

    @staticmethod
    def _is_to_foreign(payment, IBANs_own):
        IBAN_to = payment.counterparty_alias.pointer.value
        return IBAN_to not in IBANs_own

    @staticmethod
    def _get_total_expense(payments):
        """
        Sums up the values of payments in a 2d list

        Parameters
        ----------
        payments    : list[list[Payment]]

        Returns
        -------
        float       : the sum of all values of all payments
        """
        return sum([sum([float(p.amount.value) for p in batch])
                    for batch in payments])
