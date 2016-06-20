from optparse import make_option

from django.core.management.base import BaseCommand

from django_hats.roles import RoleFinder
from django_hats.utils import migrate_role, snake_case


class Command(BaseCommand):
    help = 'Migrate one role to another in the database.'
    option_list = BaseCommand.option_list + (
        make_option('-o', '--old',
                    action='store',
                    type='string',
                    dest='old_role_name',
                    help='Old Role Class Name, required'),
        make_option('-n', '--new',
                    action='store',
                    type='string',
                    dest='new_role_name',
                    help='New Role Class Name, required'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.old_role_name = None
        self.new_role_name = None

    def handle(self, *args, **options):
        print options
        old_role = RoleFinder.by_name(snake_case(options['old']))
        new_role = RoleFinder.by_name(snake_case(options['new']))

        migrate_role(old_role, new_role)
