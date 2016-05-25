from django.contrib.auth.models import Group

from django_hats.bootstrap import Bootstrapper


def synchronize_roles():
    # Get a list of the existing Roles in the system
    valid_roles = Bootstrapper.get_roles()

    # Check if the role exists in the database
    roles = Group.objects.filter(
        name__istartswith='_role_'
    ).exclude(
        id__in=[role.get_group().id for role in valid_roles]
    )

    objs = []
    # Go through all of the permissions on the groups and see if they are being used elsewhere
    # Otherwise delete them.
    for role in roles:
        for perm in role.permissions.all():
            if perm.group_set.exclude(id=role.id).exists() is False:
                objs.append(perm)
                perm.delete()

    # Delete all the roles at the end
    objs.extend(roles)
    roles.delete()

    # Create all of the new Groups
    for role in valid_roles:
        role.get_group()

    return objs
