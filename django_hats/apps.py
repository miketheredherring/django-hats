from django.apps import AppConfig

from django_hats.bootstrap import Bootstrapper


class DjangoHatsConfig(AppConfig):
    name = 'django_hats'

    def ready(self):
        Bootstrapper.load()
