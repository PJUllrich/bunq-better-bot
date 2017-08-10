from unittest import TestCase

from faker import Faker

from model import session


class BaseTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.session = session
