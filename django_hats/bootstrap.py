from importlib import import_module
import os

from django.conf import settings


class Bootstrapper(object):
    _available_roles = {}

    @staticmethod
    def load():
        # Dynamically grab package name
        package_name = os.path.dirname(__file__)

        # For each registered app, import all of the available roles
        for app in settings.INSTALLED_APPS:
            # Make sure the app is not self
            if app is not package_name:
                try:
                    import_module('.roles', app)
                except ImportError:
                    pass

    # Registers a Role with the global Bootstrapper if it is not already registered.
    # Returns the True if Role is added, None if it already exists
    @classmethod
    def register(cls, role_class):
        name = role_class.__name__.lower()

        # Make sure we haven't registered the Role already
        if name not in cls._available_roles:
            cls._available_roles[name] = role_class
            return True

    # Returns a list of available Roles
    @classmethod
    def get_roles(cls):
        return [klass for key, klass in cls._available_roles.iteritems()]
