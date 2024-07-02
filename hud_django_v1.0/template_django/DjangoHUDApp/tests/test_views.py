from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from DjangoHUDApp.models import Product, ProductCategory, ProductUsage, Warehouse, Stock, Shipment, Recipient

class UserPermissionsTest(TestCase):
    def setUp(self):
        # Create users and groups
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group.objects.create(name='Group A')
        self.user.groups.add(self.group)

        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.group2 = Group.objects.create(name='Group B')
        self.user2.groups.add(self.group2)

        # Create categories and products
        self.category = ProductCategory.objects.create(name='Category A')
        self.usage = ProductUsage.objects.create(name='Usage A')
        self.product = Product.objects.create(name='Product A', category=self.category, usage=self.usage)
        self.product.owners.add(self.group)

        # Create warehouses
        self.warehouse = Warehouse.objects.create(name='Warehouse A')
        self.warehouse.access_groups.add(self.group)

        self.recipient = Recipient.objects.create(commanding_unit='Unit A')

        # Create stock
        self.stock = Stock.objects.create(product=self.product, warehouse=self.warehouse, quantity=100)

        # Create shipment for user1
        self.shipment = Shipment.objects.create(
            user=self.user,
            shipment_type='OUT',
            recipient=self.recipient,
            date=timezone.now()
        )

    def test_user_can_only_view_their_group_products(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('DjangoHUDApp:pageProduct'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product A')

        # Ensure user2 cannot see the product
        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('DjangoHUDApp:pageProduct'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Product A')

    def test_user_can_only_view_their_group_shipments(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('DjangoHUDApp:pageOrder'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f" Αποστολή από {self.user.username}")

        # Create a shipment by another user in a different group
        Shipment.objects.create(
            user=self.user2,
            shipment_type='OUT',
            recipient=self.recipient,
            date=timezone.now()
        )

        response = self.client.get(reverse('DjangoHUDApp:pageOrder'))
        self.assertNotContains(response, f" Αποστολή από {self.user2.username}")

    def test_user_can_only_view_stock_in_their_warehouse(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('DjangoHUDApp:pageStockPerWarehouse', args=[self.warehouse.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product A')

        # Ensure user2 cannot see the stock in warehouse A
        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('DjangoHUDApp:pageStockPerWarehouse', args=[self.warehouse.name]))
        self.assertEqual(response.status_code, 403)  # Assuming forbidden access
