from django_hats.bootstrap import Bootstrapper

from tests import RolesTestCase
from tests.roles import Scientist, BadlyNamedModel


class BadRole(object):
    @classmethod
    def get_slug(cls):
        return 'scientist'


class BootstrapTestCases(RolesTestCase):
    def test_register(self):
        roles = Bootstrapper.get_roles()
        expected_roles = [Scientist, BadlyNamedModel]
        for role in expected_roles:
            self.assertTrue(role in roles)

    def test_register_multiple(self):
        self.assertRaises(ValueError, Bootstrapper.register, BadRole)
