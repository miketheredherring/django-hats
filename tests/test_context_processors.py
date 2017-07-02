from django.contrib.auth.models import User
from django.test import RequestFactory

from django_hats.context_processors import roles

from tests import RolesTestCase
from tests.roles import Scientist


class TemplateTageTestCases(RolesTestCase):
    # Tests `django_hats.templatetags.roles.roles`
    def test_roles_user(self):
        user = User.objects.create(username='tester')
        Scientist.assign(user)
        request = RequestFactory().get('/test/')
        request.user = user
        context = roles(request)
        self.assertTrue(context['roles']['scientist'])
        self.assertTrue('scientist' in context['roles'])

    # Tests `django_hats.templatetags.roles.roles`
    def test_roles_anon_user(self):
        request = RequestFactory().get('/test/')
        context = roles(request)
        self.assertFalse(context['roles']['scientist'])
