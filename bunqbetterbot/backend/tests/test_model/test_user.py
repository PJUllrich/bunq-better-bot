from model import User
from tests.rules.user import UserRule
from tests.test_base import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        try:
            user_new = UserRule.create()
            User.add(user_new)
            assert True
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
