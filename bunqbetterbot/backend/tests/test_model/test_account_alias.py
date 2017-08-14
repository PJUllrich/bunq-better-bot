from model import AccountAlias
from tests.rules.account_alias import AccountAliasRule
from tests.test_base import BaseTest


class AccountAliasTest(BaseTest):
    def test_create_account_alias(self):
        try:
            rand_account_alias = AccountAliasRule.create()
            AccountAlias.add(rand_account_alias)
            assert True
        except Exception as e:
            assert False, f'No Exception should be thrown. Exception: {str(e)}'
