import six

from django.contrib.auth.models import Group, Permission

from django_hats.bootstrap import Bootstrapper
from django_hats.utils import snake_case


class RoleMetaClass(type):
    # Called when class is imported in order to guarantee proper setup of child classes to parent
    def __new__(cls, name, bases, attrs):
        # Call to super
        super_new = super(RoleMetaClass, cls).__new__(cls, name, bases, attrs)

        # Check if the Role is registered in the global namespace
        if bases and Role in bases:
            super_new._meta = type('Meta', (), {})
            super_new._meta.permissions = ()
            # Extract potential Meta information from super
            if hasattr(super_new, 'Meta'):
                for attr in [attr for attr in dir(super_new.Meta) if not callable(attr) and not attr.startswith('__')]:
                    setattr(super_new._meta, attr, getattr(super_new.Meta, attr))

            # Register the new Role
            Bootstrapper.register(super_new)

        return super_new


class Role(six.with_metaclass(RoleMetaClass)):
    # Provides default value pre-momoization
    group = None

    # Adds the specified permission(s) to the Role
    @classmethod
    def add_permissions(cls, *args):
        return cls.get_group().permissions.add(*args)

    # Adds the specified permission(s) to the Role
    @classmethod
    def remove_permissions(cls, *args):
        return cls.get_group().permissions.remove(*args)

    # Returns True if the User is a member of this Role, else False
    @classmethod
    def check_membership(cls, user):
        return user.groups.filter(id=cls.get_group().id).exists()

    # Returns a list of Users associated with this Role
    @classmethod
    def get_users(cls):
        group = cls.get_group()
        return group.user_set.all()

    # Returns the individual Group associated with this Role
    @classmethod
    def get_group(cls):
        if cls.group is None:
            cls.group, _ = Group.objects.get_or_create(name='%s%s' % (Bootstrapper.prefix, cls.get_slug()))
        return cls.group

    # Returns a list of Permissions associated with this Role
    @classmethod
    def get_permissions(cls):
        permissions = cls.get_group().permissions.all()
        return permissions

    # Does the necessary assignment of Groups/Permissions to the User(s) in question
    @classmethod
    def assign(cls, *users):
        group = cls.get_group()
        group.user_set.add(*users)

    # Does the necessary removal of Groups/Permissions to the User in question
    @classmethod
    def remove(cls, *users):
        group = cls.get_group()
        group.user_set.remove(*users)

    # Returns a unique identifier for the Role name
    @classmethod
    def get_slug(cls):
        return (getattr(cls._meta, 'name', None) or snake_case(cls.__name__)).lower()

    # Synchronizes the Role with the database
    @classmethod
    def synchronize(cls):
        # Adds all of the permissions to the Role
        cls.add_permissions(
            *Permission.objects.filter(codename__in=cls._meta.permissions)
        )

        perms_to_remove = []
        # Check if a permission should be revoked for a group
        for perm in cls.get_permissions():
            if perm.codename not in cls._meta.permissions:
                perms_to_remove.append(perm)
        cls.remove_permissions(*perms_to_remove)


class RoleFinder(object):
    @staticmethod
    def by_name(name):
        '''Returns single `Role` where snake case name matches the given string `name`.
        '''
        return Bootstrapper._available_roles.get(name, None)

    @staticmethod
    def by_group(group):
        '''Returns single `Role` which `group` corresponds with.
        '''
        return RoleFinder.by_name(group.name.replace(Bootstrapper.prefix, ''))

    @staticmethod
    def by_user(user):
        '''Returns list of `Roles` which belong to a given `User`.
        '''
        roles = []
        for group in user.groups.filter(name__istartswith=Bootstrapper.prefix):
            role = RoleFinder.by_group(group)
            if role is not None:
                roles.append(role)
        return roles
