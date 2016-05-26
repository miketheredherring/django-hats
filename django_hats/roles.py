import six

from django.contrib.auth.models import Group
from django_hats.bootstrap import Bootstrapper


class RoleMetaClass(type):
    # Called when class is imported in order to guarantee proper setup of child classes to parent
    def __new__(cls, name, bases, attrs):
        # Call to super
        super_new = super(RoleMetaClass, cls).__new__(cls, name, bases, attrs)

        # Check if the Role is registered in the global namespace
        if bases and Role in bases:
            super_new._meta = type('Meta', (), {})
            # Extract potential Meta information from super
            if hasattr(super_new, 'Meta'):
                for attr in [attr for attr in dir(super_new.Meta) if not callable(attr) and not attr.startswith('__')]:
                    setattr(super_new._meta, attr, getattr(super_new.Meta, attr))

            # Register the new Role
            Bootstrapper.register(super_new)

        return super_new


class Role(six.with_metaclass(RoleMetaClass)):
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
        group, _ = Group.objects.get_or_create(name='_role_%s' % cls.get_slug())
        return group

    # Returns a list of Permissions associated with this Role
    @classmethod
    def get_permissions(cls):
        permissions = cls.get_group().permissions.all()
        return permissions

    # Does the necessary assignment of Groups/Permissions to the User in question
    @classmethod
    def assign(cls, user):
        group = cls.get_group()
        user.groups.add(group)

    # Does the necessary removal of Groups/Permissions to the User in question
    @classmethod
    def remove(cls, user):
        group = cls.get_group()
        user.groups.remove(group)

    # Returns a unique identifier for the Role name
    @classmethod
    def get_slug(cls):
        return (getattr(cls._meta, 'name', None) or cls.__name__).lower()


class RoleFinder(object):
    @staticmethod
    def by_name(name):
        return Bootstrapper._available_roles.get(name, None)
