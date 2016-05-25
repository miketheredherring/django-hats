import six

from django_hats.bootstrap import Bootstrapper


class RoleMetaClass(type):
    # Called when class is imported in order to guarantee proper setup of child classes to parent
    def __new__(cls, name, bases, attrs):
        # Call to super
        super_new = super(RoleMetaClass, cls).__new__(cls, name, bases, attrs)

        # Check if the Role is registered in the global namespace
        if bases and Role in bases:
            Bootstrapper.register(super_new)

        return super_new


class Role(six.with_metaclass(RoleMetaClass)):
    pass
