from django.test import TestCase

from django_hats.bootstrap import Bootstrapper

from tests.roles import Scientist, BadlyNamedModel


class BadRole(object):
    @classmethod
    def get_slug(cls):
        return 'scientist'


class BootstrapTestCases(TestCase):
    def test_register(self):
        self.assertEqual(Bootstrapper.get_roles(), [Scientist, BadlyNamedModel])

    def test_register_multiple(self):
        self.assertRaises(ValueError, Bootstrapper.register, BadRole)
