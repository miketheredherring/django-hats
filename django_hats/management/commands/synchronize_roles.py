from django.core.management.base import BaseCommand

from django_hats.utils import synchronize_roles


class Command(BaseCommand):
    help = 'Removes stale Role Groups and Permissions from the database.'

    def handle(self, *args, **options):
        synchronize_roles()
