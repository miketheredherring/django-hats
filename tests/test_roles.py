from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase

from django_hats.roles import RoleFinder

from tests.roles import GeneticCounselor, Scientist

# Assign the User model for shortcut purposes
User = get_user_model()


class BadRole(object):
    @classmethod
    def get_slug(cls):
        return 'scientist'


class RoleTestCases(TestCase):
    # Tests `django_hats.roles.Role.get_group()`
    def test_get_group(self):
        self.assertEqual(Scientist.get_group().name, '_role_scientist')
        self.assertEqual(GeneticCounselor.get_group().name, '_role_genetic_counselor')

    # Tests `django_hats.roles.Role.get_permissions()`
    def test_get_permissions(self):
        self.assertEqual(len(Scientist.get_permissions()), 0)

    # Tests `django_hats.roles.Role.assign()`
    def test_assign(self):
        user = User.objects.create(username='tester')
        self.assertEqual(user.groups.count(), 0)
        Scientist.assign(user)
        self.assertEqual(user.groups.count(), 1)
        self.assertEqual(user.groups.first(), Scientist.get_group())

    # Tests `django_hats.roles.Role.remove()`
    def test_remove(self):
        user = User.objects.create(username='tester')
        self.assertEqual(user.groups.count(), 0)
        Scientist.assign(user)
        self.assertEqual(user.groups.count(), 1)
        Scientist.remove(user)
        self.assertEqual(user.groups.count(), 0)

    # Tests `django_hats.roles.Role.get_users()`
    def test_get_users(self):
        user = User.objects.create(username='tester')
        self.assertEqual(Scientist.get_users().count(), 0)
        Scientist.assign(user)
        self.assertEqual(Scientist.get_users().count(), 1)
        Scientist.remove(user)
        self.assertEqual(Scientist.get_users().count(), 0)

    # Tests `django_hats.roles.Role.check_membership()`
    def test_check_membership(self):
        user = User.objects.create(username='tester')
        self.assertFalse(Scientist.check_membership(user))
        Scientist.assign(user)
        self.assertTrue(Scientist.check_membership(user))

    # Tests `django_hats.roles.Role.add_permissions()`
    def test_add_permissions(self):
        perm = Permission.objects.create(
            codename='temp',
            name='Temporary',
            content_type=ContentType.objects.get_for_model(User)
        )
        Scientist.add_permissions(perm)
        self.assertTrue(perm in Scientist.get_permissions())

    # Tests `django_hats.roles.Role.synchronize()`
    def test_synchronize(self):
        call_command('synchronize_roles')
        perm = Permission.objects.get(codename='change_user')
        self.assertTrue(perm in Scientist.get_permissions())

    # Tests `django_hats.roles.RoleFinder.by_user()`
    def test_rolefinder_by_user(self):
        user = User.objects.create(username='tester')
        self.assertEqual(Scientist.get_users().count(), 0)
        Scientist.assign(user)
        self.assertEqual(RoleFinder.by_user(user)[0], Scientist)
        self.assertEqual(len(RoleFinder.by_user(user)), 1)
        Scientist.remove(user)
