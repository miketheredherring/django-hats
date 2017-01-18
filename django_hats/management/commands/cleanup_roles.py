from django.core.management.base import BaseCommand

from django_hats.utils import cleanup_roles


class Command(BaseCommand):
    help = 'Removes stale Role Groups and Permissions from the database.'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # Run role cleanup
        ret = cleanup_roles()

        # Print out useful completion text
        if self.verbosity > 0:
            self.stdout.write('%(count)s roles removed' % {'count': ret[0]})
