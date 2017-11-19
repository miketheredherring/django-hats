from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from django_hats.roles import Role
from django_hats.utils import check_membership


# Checks if the defined `role_required` field is met or not
class RoleRequiredMixin(PermissionRequiredMixin):
    role_required = None
    role_required_any = False

    # Check if the User has all the necessary Permissions and is a member of the Role
    def has_permission(self):
        roles = self.get_role_required()
        user = self.request.user

        # Make sure the User belongs to all the mentioned Roles
        ret = super(RoleRequiredMixin, self).has_permission()
        ret &= check_membership(user, roles, any=self.role_required_any)
        return ret

    # Get all of the Permissions required to access this view
    def get_permission_required(self):
        # If the user has any Roles assigned to them, set permission_required = () so super doesn't error
        if self.get_role_required():
            if self.permission_required is None:
                self.permission_required = ()

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
