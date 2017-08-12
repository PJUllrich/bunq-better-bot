from model import UserSession
from tests.rules.base import BaseRule


class UserSessionRule(BaseRule):
    @classmethod
    def create(cls):
        rand_expiry = cls.faker.future_date(end_date="+5d")

        return UserSession(rand_expiry)
