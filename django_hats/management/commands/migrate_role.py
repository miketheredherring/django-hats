from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from django_hats.bootstrap import Bootstrapper
from django_hats.roles import RoleFinder
from django_hats.utils import migrate_role, snake_case


class Command(BaseCommand):
    help = 'Migrate one role to another in the database.'

    def add_arguments(self, parser):
        '''Adds command line argument options.
        '''
        parser.add_argument(
            '-o', '--old',
            action='store',
            type=str,
            dest='old',
            help='Old Role Class Name, required'
        )
        parser.add_argument(
            '-n', '--new',
            action='store',
            type=str,
            dest='new',
            help='New Role Class Name, required'
        )

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # Identifiy the two roles
        old_role = RoleFinder.by_name(snake_case(options['old']))
        new_role = RoleFinder.by_name(snake_case(options['new']))

        # If the old role can't be found, search directly for the group
        if old_role is None:
            old_group = Group.objects.get(name='%s%s' % (Bootstrapper.prefix, snake_case(options['old'])))
        else:
            old_group = old_role.get_group()

        migrate_role(old_group, new_role)

        # Print out useful completion text
        if self.verbosity > 0:
            self.stdout.write(
                'Successfully migration %(old_role)s -> %(new_role)s' % {
                    'old_role': options['old'],
                    'new_role': options['new']
                }
            )
