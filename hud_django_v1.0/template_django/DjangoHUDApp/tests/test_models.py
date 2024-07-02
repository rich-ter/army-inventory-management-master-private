from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from DjangoHUDApp.models import Product, ProductCategory, ProductUsage, Warehouse, Stock, Shipment, ShipmentItem, Recipient, ValidationError

class StockAdjustmentTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create product category and usage
        self.category = ProductCategory.objects.create(name='Category A')
        self.usage = ProductUsage.objects.create(name='Usage A')
        
        # Create a product
        self.product = Product.objects.create(name='Product A', category=self.category, usage=self.usage)
        
        # Create a warehouse
        self.warehouse = Warehouse.objects.create(name='Warehouse A')
        
        # Create a recipient
        self.recipient = Recipient.objects.create(commanding_unit='Unit A')
        
        # Create initial stock
        self.stock = Stock.objects.create(product=self.product, warehouse=self.warehouse, quantity=100)

    def test_stock_decreases_on_outgoing_shipment(self):
        # Create an outgoing shipment
        shipment = Shipment.objects.create(
            user=self.user,
            shipment_type='OUT',
            recipient=self.recipient,
            date=timezone.now()
        )

        # Add a shipment item
        ShipmentItem.objects.create(
            shipment=shipment,
            product=self.product,
            warehouse=self.warehouse,
            quantity=10
        )

        # Check stock decreases by 10
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 90)

    def test_stock_increases_on_incoming_shipment(self):
        # Create an incoming shipment
        shipment = Shipment.objects.create(
            user=self.user,
            shipment_type='IN',
            recipient=self.recipient,
            date=timezone.now()
        )

        # Add a shipment item
        ShipmentItem.objects.create(
            shipment=shipment,
            product=self.product,
            warehouse=self.warehouse,
            quantity=10
        )

        # Check stock increases by 10
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 110)

    def test_error_raised_when_insufficient_stock(self):
        # Create an outgoing shipment
        shipment = Shipment.objects.create(
            user=self.user,
            shipment_type='OUT',
            recipient=self.recipient,
            date=timezone.now()
        )

        # Attempt to create a shipment item with a quantity greater than the available stock
        with self.assertRaises(ValidationError):
            ShipmentItem.objects.create(
                shipment=shipment,
                product=self.product,
                warehouse=self.warehouse,
                quantity=200  # More than available stock
            )
