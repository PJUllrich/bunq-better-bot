from unittest import TestCase

from faker import Faker

from model import session
from run_backend import backend


class BaseTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.session = session

        self.app = backend.test_client()
        self.app.testing = True
