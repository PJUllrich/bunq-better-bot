import bcrypt

import util.security as security
from tests.test_base import BaseTest


class SecurityTest(BaseTest):
    def test_derivate_key(self):
        rand_pw = self.faker.password().encode()

        res1 = security.derivate_key(rand_pw)
        res2 = security.derivate_key(rand_pw)

        assert res1 != res2, 'Derivation of the same key twice must not lead to same hash.'

    def test_check_password(self):
        rand_pw = self.faker.password().encode()
        rand_pw_hashed = security.hash_password(rand_pw)
        assert security.check_password(rand_pw, rand_pw_hashed)
