from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib import admin
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os 
from django.db.models import Max

class Recipient(models.Model):
    commanding_unit = models.CharField(max_length=100)
    recipient_unit = models.CharField(max_length=100, default='None Specified')
    notes = models.CharField(max_length=450, null=True, blank=True)

    def __str__(self):
        return self.commanding_unit
    
    def last_shipment_date(self):
        last_shipment = self.shipmentitem_set.aggregate(last_date=Max('shipment__date'))
        return last_shipment['last_date']
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ProductUsage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def validate_image(file):
    file_size = file.size
    limit_kb = 10000
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

    if not file.name.endswith(('.jpg', '.png')):
        raise ValidationError("Μόνο αρχεία .jpg & .png επιτρέπονται")

class Product(models.Model):

    MEASUREMENT_TYPES = (
        ("ΤΕΜΑΧΙΑ", "ΤΕΜΑΧΙΑ"), 
        ("ΜΕΤΡΑ", "ΜΕΤΡΑ"),
        ("ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "ΚΑΜΙΑ ΕΠΙΛΟΓΗ"),       
    )

    name = models.CharField(max_length=100, null=False)
    batch_number = models.CharField(max_length=100, null=False, default='KAMIA EPILOGH', blank=True)
    unit_of_measurement = models.CharField(max_length=30, choices=MEASUREMENT_TYPES, default='ΚΑΜΙΑ ΕΠΙΛΟΓΗ')
    image = models.ImageField(upload_to='product_images/', validators=[validate_image], blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    usage = models.ForeignKey(ProductUsage, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    owners = models.ManyToManyField(Group, blank=True, verbose_name='Product Owners')

    def total_stock(self):
        """Return the total stock across all warehouses for this product."""
        return self.stocks.aggregate(total=Sum('quantity'))['total'] or 0

    def __str__(self):
        return f"{self.name} - {self.category}"

@receiver(post_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
def validate_shipment_attachment(file):
    file_size = file.size
    limit_kb = 10000
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)

    if not file.name.endswith(('.pdf')):
        raise ValidationError("Μόνο αρχεία pdf")

class Shipment(models.Model):
    SHIPMENT_TYPE_CHOICES = [
        ('IN', 'Εισερχόμενη'),
        ('OUT', 'Εξερχόμενη'),
    ]

    SHIPMENT_METHOD_CHOICES = [
        ('ΥΕΣΑ', 'ΥΕΣΑ'),
        ('ΚΡΥΠΤΟΔΙΑΥΛΟΣ', 'ΚΡΥΠΤΟΔΙΑΥΛΟΣ'),
        ('ΠΑΡΑΛΑΒΗ ΑΠΟ ΕΞΟΥΣΙΟΔΟΤΗΜΕΝΟ ΠΡΟΣΩΠΙΚΟ', 'ΠΑΡΑΛΑΒΗ ΑΠΟ ΕΞΟΥΣΙΟΔΟΤΗΜΕΝΟ ΠΡΟΣΩΠΙΚΟ'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipments')
    shipment_type = models.CharField(max_length=3, choices=SHIPMENT_TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    notes = models.CharField(max_length=200, null=True, blank=True)
    attachment = models.FileField(upload_to='shipment_attachments/', validators=[validate_shipment_attachment], null=True, blank=True)
    order_number = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.notes is None:
            self.notes = ''
        super().save(*args, **kwargs)

    def __str__(self):
        return f" Αποστολή από {self.user} / Τύπου: {self.shipment_type} - Ημερομηνία: {self.date}"

@receiver(post_delete, sender=Shipment)
def delete_shipment_files(sender, instance, **kwargs):
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    access_groups = models.ManyToManyField(Group, related_name="access_warehouses")

    def __str__(self):
        return f"{self.name}"

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='shipment_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity} in {self.shipment}"

    def clean(self):
        """Ensure stock validation before saving the shipment item."""
        if self.shipment.shipment_type == 'OUT':
            stock = Stock.objects.get(product=self.product, warehouse=self.warehouse)
            if stock.quantity < self.quantity:
                raise ValidationError(f'Insufficient stock for {self.product.name} in {self.warehouse.name}. Cannot proceed with the operation.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, skip_validation=False, **kwargs):
        if not skip_validation:
            self.clean()
        super().delete(*args, **kwargs)

@receiver(post_save, sender=ShipmentItem)
def adjust_stock_on_save(sender, instance, created, **kwargs):
    adjust_stock(instance, created=True)

@receiver(post_delete, sender=ShipmentItem)
def adjust_stock_on_delete(sender, instance, **kwargs):
    adjust_stock(instance, created=False)

def adjust_stock(instance, created):
    with transaction.atomic():
        stock, _ = Stock.objects.get_or_create(
            product=instance.product,
            warehouse=instance.warehouse,
            defaults={'quantity': 0}
        )

        # Determine the adjustment direction based on the shipment type
        if instance.shipment.shipment_type == 'IN':
            adjustment = instance.quantity if created else -instance.quantity
        elif instance.shipment.shipment_type == 'OUT':
            adjustment = -instance.quantity if created else instance.quantity

        # Apply the adjustment
        stock.quantity += adjustment

        # Prevent stock from going negative for 'OUT' shipments
        if stock.quantity < 0:
            raise ValidationError(f'Insufficient stock for {instance.product.name} in {instance.warehouse.name}. Cannot proceed with the operation.')

        stock.save()

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f"{self.product.name} in {self.warehouse.name} - Qty: {self.quantity}"
