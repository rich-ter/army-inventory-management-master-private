from django.test import TestCase
from .models import Product, Warehouse, Stock, Shipment
from django.db.models import F

class StockManagementTests(TestCase):
    def setUp(self):
        # Create test data
        self.warehouse = Warehouse.objects.create(name="Main Warehouse", location="Downtown")
        self.product = Product.objects.create(name="Laptop", category="Electronics", usage="Office")
        self.stock = Stock.objects.create(product=self.product, warehouse=self.warehouse, quantity=100)

    def test_add_stock(self):
        # Test addition of stock
        self.stock.quantity += 50
        self.stock.save()
        updated_stock = Stock.objects.get(id=self.stock.id)
        self.assertEqual(updated_stock.quantity, 150)

    def test_subtract_stock(self):
        # Test subtraction of stock
        self.stock.quantity -= 30
        self.stock.save()
        updated_stock = Stock.objects.get(id=self.stock.id)
        self.assertEqual(updated_stock.quantity, 70)

    def test_shipment_outgoing_impacts_stock(self):
        # Test that an outgoing shipment reduces stock appropriately
        shipment = Shipment.objects.create(shipment_type='OUT', user_id=1)  # assuming user_id=1 is valid
        self.stock.ship(shipment, 20)
        self.assertEqual(Stock.objects.get(id=self.stock.id).quantity, 80)

    def test_shipment_incoming_impacts_stock(self):
        # Test that an incoming shipment increases stock appropriately
        shipment = Shipment.objects.create(shipment_type='IN', user_id=1)  # assuming user_id=1 is valid
        self.stock.receive(shipment, 20)
        self.assertEqual(Stock.objects.get(id=self.stock.id).quantity, 120)

    def test_concurrent_stock_update(self):
        # Test handling of concurrent stock updates
        original_quantity = self.stock.quantity
        Stock.objects.filter(id=self.stock.id).update(quantity=F('quantity') + 50)
        Stock.objects.filter(id=self.stock.id).update(quantity=F('quantity') - 30)
        expected_quantity = original_quantity + 20
        self.assertEqual(Stock.objects.get(id=self.stock.id).quantity, expected_quantity)

