import os

from tests.test_base import BaseTest
from util import security


class SecurityTest(BaseTest):
    def test_derivate_key(self):
        rand_pw = security.gen_token()

        res1 = security.derivate_key(rand_pw)
        res2 = security.derivate_key(rand_pw)

        assert res1 != res2, 'Derivation of the same key twice must not lead to same hash.'

    def test_encryption_and_decryption(self):
        rand_text = self.faker.text()
        rand_key = security.gen_token()

        text_encrypted, iv = security.encrypt(rand_text, rand_key)
        text_decrypted = security.decrypt(text_encrypted, rand_key, iv)

        assert text_decrypted == rand_text, 'Decrypted text must match plain text.'
