import bcrypt

import util.security as security
from test.test_base import BaseTest


class SecurityTest(BaseTest):
    def test_hash_password(self):
        rand_pw = self.faker.password().encode()
        rand_pw_hashed = security.derivate_key(rand_pw)
        assert bcrypt.checkpw(rand_pw, rand_pw_hashed)

    def test_check_password(self):
        rand_pw = self.faker.password().encode()
        rand_pw_hashed = bcrypt.hashpw(rand_pw, bcrypt.gensalt())
        assert security.check_password(rand_pw, rand_pw_hashed)
