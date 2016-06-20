from django.core.management.base import BaseCommand

from django_hats.bootstrap import Bootstrapper
from django_hats.utils import synchronize_roles


class Command(BaseCommand):
    help = 'Synchronizes Role Groups and Permissions with the database.'

    def handle(self, *args, **options):
        roles = Bootstrapper.get_roles()
        synchronize_roles(roles)
