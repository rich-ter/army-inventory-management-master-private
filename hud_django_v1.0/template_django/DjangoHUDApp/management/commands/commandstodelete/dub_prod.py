import logging
from django.core.management.base import BaseCommand
from DjangoHUDApp.models import Product

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('identify_duplicates.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = 'Identify duplicate products in the database'

    def handle(self, *args, **kwargs):
        # Fetch all products
        products = Product.objects.all()

        # Dictionaries to track duplicates
        name_dict = {}
        batch_number_dict = {}

        duplicates = []

        # Iterate through all products to find duplicates
        for product in products:
            if product.name in name_dict:
                name_dict[product.name].append(product)
            else:
                name_dict[product.name] = [product]

            if product.batch_number in batch_number_dict:
                batch_number_dict[product.batch_number].append(product)
            else:
                batch_number_dict[product.batch_number] = [product]

        # Identify duplicates by name
        for name, items in name_dict.items():
            if len(items) > 1:
                duplicates.extend(items)
                logger.info(f"Duplicate products found with name '{name}': {[item.id for item in items]}")

        # Identify duplicates by batch number
        for batch_number, items in batch_number_dict.items():
            if len(items) > 1:
                duplicates.extend(items)
                logger.info(f"Duplicate products found with batch number '{batch_number}': {[item.id for item in items]}")

        # Remove duplicates from the list
        duplicates = list(set(duplicates))

        # Print or log the duplicate products
        if duplicates:
            self.stdout.write(self.style.WARNING(f'Found {len(duplicates)} duplicate products. See identify_duplicates.log for details.'))
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate products found.'))
