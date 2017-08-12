from model import AccountReference
from tests.rules.base import BaseRule
from tests.rules.monetary_account_bank import MonetaryAccountBankRule


class AccountReferenceRule(BaseRule):
    @classmethod
    def create(cls):
        rand_account = MonetaryAccountBankRule.create()
        return AccountReference(rand_account)
