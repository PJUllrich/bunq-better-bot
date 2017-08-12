from model import AccountAlias
from tests.rules.base import BaseRule


class AccountAliasRule(BaseRule):
    @classmethod
    def create(cls):
        return AccountAlias(cls.faker.ean(), cls.faker.name())
