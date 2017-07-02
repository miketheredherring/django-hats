from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

from django_hats.mixins import RoleRequiredMixin

from tests import RolesTestCase
from tests.roles import Scientist


class Object(object):
    pass


class MixinTestCases(RolesTestCase):
    # Tests `django_hats.mixins.RoleRequiredMixin.get_role_required()`
    def test_get_role_required(self):
        mixin = RoleRequiredMixin()
        self.assertRaises(ImproperlyConfigured, mixin.get_role_required)
        mixin.role_required = Scientist
        self.assertEqual(mixin.get_role_required(), (Scientist, ))
        mixin.role_required = (Scientist, )
        self.assertEqual(mixin.get_role_required(), (Scientist, ))

    # Tests `django_hats.mixins.RoleRequiredMixin.get_permission_required()`
    def test_get_permission_required(self):
        mixin = RoleRequiredMixin()
        self.assertRaises(ImproperlyConfigured, mixin.get_permission_required)
        mixin.role_required = Scientist
        self.assertEqual(len(mixin.get_permission_required()), 0)

    # Tests `django_hats.mixins.RoleRequiredMixin.has_permission()`
    def test_has_permission(self):
        user = User.objects.create(username='tester')
        mixin = RoleRequiredMixin()
        mixin.request = Object()
        mixin.request.user = user
        mixin.role_required = Scientist
        self.assertFalse(mixin.has_permission())
        Scientist.assign(user)
        self.assertTrue(mixin.has_permission())
