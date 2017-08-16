import json
import os
import random

from model import User
from tests.test_base import BaseTest


class AccountTest(BaseTest):
    def setUp(self):
        super().setUp()

        self._API_KEY = os.environ['BUNQ_BOT_TEST_API_KEY']

    def test_register(self):
        rand_data = self._get_random_registration_data()
        rand_chat_id = int(rand_data['chat_id'])

        res = self.app.post('/user/register', data=json.dumps(rand_data))
        assert res.status_code == 201

        user = User.qry_by('chat_id', rand_chat_id).first()
        assert user is not None

    def test_login(self):
        rand_auth = {
            'chat_id': random.randint(1000, 1000000),
            'pw': self.faker.password()
        }

        # Error should be returned since no user with rand_chat_id is yet in the database
        res = self.app.post('/user/login', data=json.dumps(rand_auth))
        assert res.status_code == 401

        rand_data = self._get_random_registration_data()
        res = self.app.post('/user/register', data=json.dumps(rand_data))
        assert res.status_code == 201

        rand_auth['chat_id'] = rand_data['chat_id']

        # Error should be returned since the user exists, but the password does not match
        res = self.app.post('/user/login', data=json.dumps(rand_auth))
        assert res.status_code == 401

        rand_auth['pw'] = rand_data['pw']

        # Success should be returned since both the chat_id and password match the records
        res = self.app.post('/user/login', data=json.dumps(rand_auth))
        assert res.status_code == 200

    def _get_random_registration_data(self):
        rand_env = 'SANDBOX'
        rand_chat_id = random.randint(1000, 1000000)
        rand_pw = self.faker.password()

        return {
            'env': rand_env,
            'chat_id': rand_chat_id,
            'pw': rand_pw,
            'api_key': self._API_KEY
        }
