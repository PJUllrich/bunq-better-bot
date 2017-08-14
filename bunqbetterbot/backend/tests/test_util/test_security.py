import os

from tests.test_base import BaseTest
from util import security


class SecurityTest(BaseTest):
    def test_derivate_key(self):
        rand_pw = self.faker.password()

        res1 = security.derivate_key(rand_pw)
        res2 = security.derivate_key(rand_pw)

        assert res1 != res2, 'Derivation of the same key twice must not lead to same hash.'

    def test_encryption_and_decryption(self):
        rand_text = self.faker.text()
        rand_key = os.urandom(32)

        text_encrypted, iv = security.encrypt(rand_text, rand_key)
        text_decrypted_bytes = security.decrypt(text_encrypted, rand_key, iv)

        text_decrypted = text_decrypted_bytes.decode()

        assert text_decrypted == rand_text, 'Decrypted text must match plain text.'
