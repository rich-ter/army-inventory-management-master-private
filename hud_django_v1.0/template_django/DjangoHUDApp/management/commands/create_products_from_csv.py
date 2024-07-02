import csv
import os
import logging
from django.core.management.base import BaseCommand
from DjangoHUDApp.models import Product, ProductCategory, ProductUsage, Warehouse, Stock
from django.contrib.auth.models import Group
from django.db import transaction

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('import_products.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_csv = os.path.join(base_dir, 'all_product_data.csv')

        expected_columns = ["batch_number", "name", "unit_of_measurement", "description", "category", "usage", "owner", "quantity"]

        total_rows = 0
        imported_rows = 0
        error_count = 0

        initial_product_count = Product.objects.count()

        with open(input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Skip header row

            logger.debug(f"Header columns: {header}")

            for row in reader:
                total_rows += 1

                row_original = row.copy()  # Save the original row for logging purposes

                if len(row) < len(expected_columns):
                    row.extend([''] * (len(expected_columns) - len(row)))
                elif len(row) > len(expected_columns):
                    row = row[:len(expected_columns)]

                batch_number, name, unit_of_measurement, description, category_name, usage_name, owner_name, quantity = row

                logger.debug(f"Processing row {total_rows}: {row_original}")

                try:
                    with transaction.atomic():
                        # Create or get the related objects
                        try:
                            category, _ = ProductCategory.objects.get_or_create(name=category_name)
                        except Exception as e:
                            logger.error(f'Error creating/getting category for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        try:
                            usage, _ = ProductUsage.objects.get_or_create(name=usage_name)
                        except Exception as e:
                            logger.error(f'Error creating/getting usage for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        try:
                            owner_group, _ = Group.objects.get_or_create(name=owner_name)
                        except Exception as e:
                            logger.error(f'Error creating/getting owner group for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        try:
                            product = Product.objects.create(
                                batch_number=batch_number,
                                name=name,
                                unit_of_measurement=unit_of_measurement,
                                description=description,
                                category=category,
                                usage=usage
                            )
                            product.owners.add(owner_group)
                            imported_rows += 1
                            message = f'Successfully imported row {total_rows}: {row_original}'
                            logger.info(message)
                        except Exception as e:
                            logger.error(f'Error creating product for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        # Determine the warehouse based on the owner
                        if owner_name == "ΔΟΡΥΦΟΡΙΚΑ":
                            warehouse_name = "ΔΟΡΥΦΟΡΙΚΑ"
                        elif owner_name == "ΔΙΔΕΣ":
                            warehouse_name = "ΚΕΠΙΚ"
                        else:
                            raise ValueError(f'Unknown owner: {owner_name}')

                        try:
                            warehouse, _ = Warehouse.objects.get_or_create(name=warehouse_name)
                        except Exception as e:
                            logger.error(f'Error creating/getting warehouse for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        # Update the stock for the product in the determined warehouse
                        try:
                            quantity = int(quantity)
                            stock, created = Stock.objects.get_or_create(product=product, warehouse=warehouse)
                            if created:
                                stock.quantity = quantity
                            else:
                                stock.quantity += quantity
                            stock.save()
                        except Exception as e:
                            logger.error(f'Error updating stock for row {total_rows}: {row_original}. Exception: {e}')
                            raise

                        logger.debug(f"Completed transaction for row {total_rows}")
                except Exception as e:
                    error_count += 1
                    message = f'Error processing row {total_rows}: {row_original}. Exception: {e}'
                    logger.error(message)

        final_product_count = Product.objects.count()

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_rows} out of {total_rows} products from CSV file'))
        self.stdout.write(self.style.ERROR(f'{error_count} rows encountered errors during import. See import_products.log for details.'))
        self.stdout.write(self.style.WARNING(f'Initial product count: {initial_product_count}, Final product count: {final_product_count}'))

        logger.info(f'Initial product count: {initial_product_count}, Final product count: {final_product_count}')
        logger.info(f'Successfully imported {imported_rows} out of {total_rows} products from CSV file')
        logger.error(f'{error_count} rows encountered errors during import. See import_products.log for details.')
