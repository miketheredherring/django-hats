from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase

from tests.roles import Scientist

# Assign the User model for shortcut purposes
User = get_user_model()


class ManagementTestCases(TestCase):
    # Tests `django_hats.management.commands.synchronize_roles`
    def test_synchronize_roles(self):
        group = Scientist.get_group()
        group.permissions.add(Permission.objects.create(codename='temporary', content_type=ContentType.objects.get_for_model(User)))
        permission_count = Permission.objects.count()
        Scientist._meta.name = '404'
        call_command('synchronize_roles')
        self.assertEqual(Group.objects.count(), 3)
        self.assertTrue(Group.objects.get(name__icontains=Scientist.get_slug()))
        self.assertEqual(Permission.objects.count(), permission_count)
        Scientist._meta.name = 'scientist'
