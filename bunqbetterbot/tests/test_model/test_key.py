from model import Key
from tests.rules.key import KeyRule
from tests.test_base import BaseTest


class KeyTest(BaseTest):
    def test_create_key(self):
        try:
            rand_key = KeyRule.create()
            Key.add(rand_key)
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
