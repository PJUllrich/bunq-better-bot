from model import Callback
from tests.rules.callback import CallbackRule
from tests.test_base import BaseTest


class CallbackTest(BaseTest):
    def test_create_callback(self):
        try:
            rand_callback = CallbackRule.create()
            Callback.add(rand_callback)
        except Exception as e:
            assert False, f'No Exception should occur. Exception: {str(e)}'
