from django_hats.roles import RoleFinder


class RolesLookup(object):
    def __init__(self, user):
        self.user = user

    def __getitem__(self, role):
        role = RoleFinder.by_name(role)
        return role.check_membership(self.user) if role is not None else False

    def __contains__(self, role):
        return self[role]


# Returns a lookup roles for Roles in the context, akin to perms for Permissions
def roles(request):
    # Only authenticated users should be checked
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()

    return {
        'roles': RolesLookup(user),
    }
