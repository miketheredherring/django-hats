import re

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from django_hats.bootstrap import Bootstrapper


def cleanup_roles():
    roles = Bootstrapper.get_roles()

    # Get stale Roles
    stale_roles = Group.objects.filter(
        name__istartswith='_role_'
    ).exclude(
        id__in=[role.get_group().id for role in roles]
    )

    perms_to_remove = []
    # Check if a permission should be revoked for a group
    for role in roles:
        for perm in role.get_permissions():
            if perm.codename not in role._meta.permissions:
                perms_to_remove.append(perm)
    role.remove_permissions(*perms_to_remove)

    # Delete all the roles at the end
    stale_roles.delete()

    return stale_roles


def synchronize_roles(roles):
    # Ensure the ContentType exists
    ContentType.objects.get_or_create(app_label='roles', model='role')

    # Create all of the new Groups
    for role in roles:
        role.synchronize()


def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
