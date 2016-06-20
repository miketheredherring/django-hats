from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_hats.bootstrap import Bootstrapper
from django_hats.utils import cleanup_roles, migrate_role, synchronize_roles

from tests.roles import GeneticCounselor, Scientist

# Assign the User model for shortcut purposes
User = get_user_model()


class UtilTestCases(TestCase):
    # Tests `django_hats.utils.migrate_role()`
    def test_migrate_role(self):
        user = User.objects.create(username='tester')
        GeneticCounselor.assign(user)
        self.assertEqual(GeneticCounselor.get_group().user_set.count(), 1)
        self.assertEqual(Scientist.get_group().user_set.count(), 0)
        migrate_role(GeneticCounselor, Scientist)
        self.assertEqual(GeneticCounselor.get_group().user_set.count(), 0)
        self.assertEqual(Scientist.get_group().user_set.count(), 1)

    # Tests `django_hats.utils.synchronize_roles()`
    def test_synchronize_roles(self):
        roles = Bootstrapper.get_roles()
        group = Scientist.get_group()
        group.permissions.add(Permission.objects.create(codename='temporary', content_type=ContentType.objects.get_for_model(User)))
        permission_count = Permission.objects.count()
        Scientist._meta.name = '404'
        synchronize_roles(roles)
        self.assertEqual(Group.objects.count(), 4)
        self.assertTrue(Group.objects.get(name__icontains=Scientist.get_slug()))
        self.assertEqual(Permission.objects.count(), permission_count)
        Scientist._meta.name = 'scientist'

    # Tests `django_hats.utils.cleanup_roles()`
    def test_cleanup_roles(self):
        roles = Bootstrapper.get_roles()
        group = Scientist.get_group()
        group.permissions.add(Permission.objects.create(codename='temporary', content_type=ContentType.objects.get_for_model(User)))
        permission_count = Permission.objects.count()
        Scientist._meta.name = '404'
        synchronize_roles(roles)
        Scientist._meta.permissions = ()
        cleanup_roles()
        self.assertEqual(Group.objects.count(), 3)
        self.assertTrue(Group.objects.get(name__icontains=Scientist.get_slug()))
        self.assertRaises(Group.DoesNotExist, Group.objects.get, name__icontains='scientist')
        self.assertEqual(Permission.objects.count(), permission_count)
        Scientist._meta.name = 'scientist'
        Scientist._meta.permissions = ('change_user', )
