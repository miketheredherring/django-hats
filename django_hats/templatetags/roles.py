import six

from django import template

from django_hats.roles import RoleFinder

register = template.Library()


@register.filter
def has_role(user, role):
    if isinstance(role, six.string_types):
        role = RoleFinder.by_name(role)
    return role.check_membership(user)
