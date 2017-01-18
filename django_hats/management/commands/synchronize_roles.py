from django.core.management.base import BaseCommand

from django_hats.apps import DjangoHatsConfig
from django_hats.bootstrap import Bootstrapper
from django_hats.signals import post_synchronize_roles
from django_hats.utils import synchronize_roles


class Command(BaseCommand):
    help = 'Synchronizes Role Groups and Permissions with the database.'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # Run role DB synchronization
        roles = Bootstrapper.get_roles()
        synchronize_roles(roles)

        # Emit the post-signal for apps to hook
        post_synchronize_roles.send(
            sender=DjangoHatsConfig
        )

        # Print out useful completion text
        if self.verbosity > 0:
            self.stdout.write('Role synchronization complete.')
