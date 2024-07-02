from django.contrib import admin
from .models import Product, Warehouse, Recipient, Shipment, ShipmentItem, Stock
from django.core.exceptions import ValidationError
from .models import Product, ProductCategory, ProductUsage

class ShipmentItemInline(admin.TabularInline):
    model = ShipmentItem
    extra = 1  # Number of empty forms to display

class ShipmentAdmin(admin.ModelAdmin):
    inlines = [ShipmentItemInline,]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ProductUsage)
class ProductUsageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'usage', 'description')
    search_fields = ['name']  # Enables search by product name

admin.site.register(Warehouse)
admin.site.register(Recipient)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Stock)
admin.site.register(ShipmentItem)
