from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from DjangoHUDApp.models import Warehouse

class Command(BaseCommand):
    help = 'Creates user groups and users, then assigns users to groups'

    def handle(self, *args, **options):
        # Create groups
        group_dides, _ = Group.objects.get_or_create(name='ΔΙΔΕΣ')
        group_doriforika, _ = Group.objects.get_or_create(name='ΔΟΡΥΦΟΡΙΚΑ')
        
        # Define user data
        user_data = [
            {'username': 'alexandris', 'password': 'alexandris', 'group': group_doriforika},
            {'username': 'tsaprounis', 'password': 'tsaprounis', 'group': group_dides},
            {'username': 'nikolaidis', 'password': 'nikolaidis', 'group': group_dides},
            {'username': 'raftogiannis', 'password': 'raftogiannis', 'group': group_dides},
        ]

        warehouses_data = [
            {'name': 'ΚΕΠΙΚ', 'description': 'Αποθήκη ΚΕΠΙΚ / 1ού Λόχου', 'access_groups': [group_dides]},
            {'name': 'ΤΑΓΜΑ', 'description': 'Αποθήκη ΤΔΒ 487', 'access_groups': [group_dides]},
            {'name': 'ΔΟΡΥΦΟΡΙΚΑ', 'description': 'Αποθήκη Δορυφορικών / 2ού Λόχου', 'access_groups': [group_doriforika]},
        ]

        # Create users and assign to groups
        for user_info in user_data:
            user, created = User.objects.get_or_create(username=user_info['username'])
            if created:
                user.set_password(user_info['password'])
                user.save()
                user.groups.add(user_info['group'])
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username} and added to {user_info["group"].name}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))
        
        # Create warehouses and assign to groups
        for warehouse_data in warehouses_data:
            warehouse, created = Warehouse.objects.get_or_create(
                name=warehouse_data["name"],
                defaults={"description": warehouse_data["description"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created warehouse: {warehouse.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Warehouse already exists: {warehouse.name}'))

            # Assign groups to the warehouse
            for group in warehouse_data["access_groups"]:
                warehouse.access_groups.add(group)

        self.stdout.write(self.style.SUCCESS('Successfully ensured all warehouses are created and assigned to groups.'))
