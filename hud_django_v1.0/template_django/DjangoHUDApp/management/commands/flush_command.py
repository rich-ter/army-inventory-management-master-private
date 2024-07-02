import sys
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction

class Command(BaseCommand):
    help = 'Flush specific tables in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'tables',
            nargs='*',
            type=str,
            help='Names of the tables to flush.'
        )

    def handle(self, *args, **options):
        tables = options['tables']
        if not tables:
            self.stdout.write(self.style.ERROR('No table names provided.'))
            sys.exit(1)

        # List of models in the correct deletion order (reverse of foreign key dependencies)
        models_order = [
            'Stock',
            'ShipmentItem',
            'Shipment',
            'Product',
            'Recipient',
            'Warehouse',
        ]

        models_order = [model_name for model_name in models_order if model_name in tables]

        for model_name in models_order:
            try:
                model = apps.get_model('DjangoHUDApp', model_name)
                with transaction.atomic():
                    if model_name == 'ShipmentItem':
                        for item in model.objects.all():
                            item.delete(skip_validation=True)
                    else:
                        model.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(f'Successfully flushed table: {model_name}'))
            except LookupError:
                self.stdout.write(self.style.ERROR(f'Model {model_name} not found.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error flushing table {model_name}: {e}'))
