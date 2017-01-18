from optparse import make_option

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from django_hats.bootstrap import Bootstrapper
from django_hats.roles import RoleFinder
from django_hats.utils import migrate_role, snake_case


class Command(BaseCommand):
    help = 'Migrate one role to another in the database.'
    option_list = BaseCommand.option_list + (
        make_option('-o', '--old',
                    action='store',
                    type='string',
                    dest='old',
                    help='Old Role Class Name, required'),
        make_option('-n', '--new',
                    action='store',
                    type='string',
                    dest='new',
                    help='New Role Class Name, required'),
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
