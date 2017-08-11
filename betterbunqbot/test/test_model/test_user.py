from model.user import User
from test.rules.user import UserRule
from test.test_base import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        try:
            user_new = UserRule.create()
            User.add_user(user_new)
            assert True
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
