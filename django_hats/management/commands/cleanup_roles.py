from django.core.management.base import BaseCommand

from django_hats.utils import cleanup_roles


class Command(BaseCommand):
    help = 'Removes stale Role Groups and Permissions from the database.'

    def handle(self, *args, **options):
        ret = cleanup_roles()

        print '%(count)s roles removed' % {'count': ret[0]}
