from django.conf import settings
from django.test import TestCase

from django_hats.bootstrap import Bootstrapper

from tests.roles import Scientist


class BootstrapTestCases(TestCase):
    def test_register(self):
        self.assertEqual(Bootstrapper.get_roles(), [Scientist, ])
