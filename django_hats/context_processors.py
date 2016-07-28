from django_hats.roles import RoleFinder


class RolesLookup(object):
    def __init__(self, user):
        self.user = user
        self._cache = {}

    def __getitem__(self, role_name):
        # Check if the cache has our answer
        if self._cache.get(role_name, None) is None:
            role = RoleFinder.by_name(role_name)
            self._cache[role.get_slug()] = role.check_membership(self.user) if role is not None else False

        # Return the cached role
        return self._cache[role_name]

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
