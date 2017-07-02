from django.test import TestCase

from django_hats.bootstrap import Bootstrapper


class RolesTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        '''Clears `Roles` cache for testing.
        '''
        for role in Bootstrapper.get_roles():
            setattr(role, 'group', None)
        return super(RolesTestCase, self).setUp(*args, **kwargs)
