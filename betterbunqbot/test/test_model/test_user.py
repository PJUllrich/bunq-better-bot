from model.user import User
from test.test_model.test_base import BaseTest


class UserTest(BaseTest):

    def test_create_user(self):
        rand_phone = self.faker.phone_number()
        rand_password = self.faker.sha256()
        rand_key = self.faker.sha256()

        try:
            user_new = User(rand_phone, rand_password, rand_key)
            self.session.add(user_new)
            assert True
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
