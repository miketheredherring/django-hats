from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase

from django_hats.templatetags.roles import has_role

from tests.roles import Scientist


class TemplateTageTestCases(TestCase):
    # Tests `django_hats.templatetags.roles.has_role`
    def test_has_role(self):
        user = User.objects.create(username='tester')
        self.assertFalse(has_role(user, 'scientist'))
        Scientist.assign(user)
        self.assertTrue(has_role(user, Scientist))

    # Tests `django_hats.templatetags.roles.has_role`
    def test_has_role_anonymous(self):
        self.assertFalse(has_role(AnonymousUser(), 'scientist'))
