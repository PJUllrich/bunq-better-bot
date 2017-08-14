from model import AccountReference
from tests.rules.account_reference import AccountReferenceRule
from tests.test_base import BaseTest


class AccountReferenceTest(BaseTest):
    def test_create_account(self):
        try:
            rand_account_ref = AccountReferenceRule.create()
            AccountReference.add(rand_account_ref)
            assert True
        except Exception as e:
            assert False, f'No Exception should be thrown. Exception: {str(e)}'
