import six

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
    # Returns a unique identifier for the Role name
    @classmethod
    def get_slug(cls):
        return (getattr(cls._meta, 'name', None) or cls.__name__).lower()
