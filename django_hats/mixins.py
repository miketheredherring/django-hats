from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured

from django_hats.roles import Role


# Checks if the defined `role_required` field is met or not
class RoleRequiredMixin(PermissionRequiredMixin):
    role_required = None

    # Check if the User has all the necessary Permissions and is a member of the Role
    def has_permission(self):
        roles = self.get_role_required()
        user = self.request.user

        # Make sure the User belongs to all the mentioned Roles
        ret = super(RoleRequiredMixin, self).has_permission()
        for role in roles:
            ret &= role.check_membership(user)
        return ret

    # Get all of the Permissions required to access this view
    def get_permission_required(self):
        # Assemble all of the Permissions related to the Roles
        _role_perms = Permission.objects.none()
        for role in self.get_role_required():
            _role_perms = _role_perms & role.get_permissions()
        perms = [perm.codename for perm in _role_perms]

        print perms

        # Have permissions be defined already?
        try:
            perms = perms + super(RoleRequiredMixin, self).get_permission_required()
        except ImproperlyConfigured:
            pass    # We can still have Roles

        # Reassign the permissions to include new Role ones
        self.permission_required = perms

        return super(RoleRequiredMixin, self).get_permission_required()

    # Make a tuple of the Roles needed to access this view
    def get_role_required(self):
        # Make sure roles are available to check for
        if self.role_required is None:
            raise ImproperlyConfigured(
                '{0} is missing `role_required`. Define {0}.role_required, or override '
                '{0}.get_role_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.role_required, tuple) is False and issubclass(self.role_required, Role):
            roles = (self.role_required, )
        else:
            roles = self.role_required

        return roles
