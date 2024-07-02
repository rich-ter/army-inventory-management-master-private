import csv
import os
import logging
from django.core.management import BaseCommand, CommandError, call_command
from django.contrib.auth.models import User

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('import_products.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = 'Runs all the specified management commands in order and creates a superuser'

    def handle(self, *args, **options):
        commands = [
            'create_recipients',
            'create_groups_users_warehouses',
            'create_products_from_csv'
        ]

        for command in commands:
            self.stdout.write(f'Running {command}...')
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f'Successfully ran {command}'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'Error running {command}: {e}'))
                raise CommandError(f'Error running {command}: {e}')

        # Create superuser with admin/admin credentials
        self.create_superuser()

        self.stdout.write(self.style.SUCCESS('All commands have been executed successfully'))

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
