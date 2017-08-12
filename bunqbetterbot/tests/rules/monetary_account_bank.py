from collections import namedtuple

import random

from tests.rules.account_alias import AccountAliasRule
from tests.rules.base import BaseRule


class MonetaryAccountBankRule(BaseRule):
    MonetaryAccountBankMock = namedtuple('MonetaryAccountBankMock',
                                         ['id_', 'description', 'alias'])

    @classmethod
    def create(cls):
        rand_id = random.randint(1000, 100000)
        rand_desc = cls.faker.text()
        rand_alias = AccountAliasRule.create()

        return cls.MonetaryAccountBankMock(rand_id, rand_desc, rand_alias)
