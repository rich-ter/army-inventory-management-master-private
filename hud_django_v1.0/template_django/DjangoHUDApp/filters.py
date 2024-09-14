# filters.py
import django_filters
from .models import Product, Shipment, ProductCategory, ProductUsage, Recipient, Stock
from django.db.models import Q
from unidecode import unidecode
from django import forms
from django.db.models.functions import Lower

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label='Search')

    class Meta:
        model = Product
        fields = ['name', 'category', 'usage', 'description']

    def filter_by_all(self, queryset, name, value):
        if not value:
            return queryset

        # Normalize the input by stripping whitespace
        value_normalized = value.strip()

        # Split the search term into individual words
        search_terms = value_normalized.split()

        # Build a Q object to perform partial matches for each word in search_terms
        query = Q()
        for term in search_terms:
            query |= (
                Q(name__icontains=term) |
                Q(category__name__icontains=term) |
                Q(usage__name__icontains=term) |
                Q(description__icontains=term)
            )

        # Apply the Q object to the queryset
        return queryset.filter(query)

class ShipmentFilter(django_filters.FilterSet):
    order_number = django_filters.CharFilter(field_name='id', lookup_expr='exact', label='Order Number')
    recipient = django_filters.ModelChoiceFilter(queryset=Recipient.objects.all(), label='Recipient')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='Από')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='Έως')

    class Meta:
        model = Shipment
        fields = ['shipment_type', 'recipient', 'order_number', 'start_date', 'end_date', 'notes']


class RecipientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label='Search')

    class Meta:
        model = Recipient
        fields = []

    def normalize_input(self, value):
        # Normalize the input to ensure case insensitivity and remove accents
        return unidecode(value.strip().lower())

    def filter_by_all(self, queryset, name, value):
        if not value:
            return queryset
        
        normalized_value = self.normalize_input(value)
        print(f"Normalized Search Value: {normalized_value}")  # Debugging line

        # Use both icontains and iexact for better precision
        filtered_queryset = queryset.filter(
            Q(commanding_unit__icontains=normalized_value) |
            Q(recipient_unit__icontains=normalized_value) |
            Q(commanding_unit__iexact=value) |  # Exact match for the original input
            Q(recipient_unit__iexact=value)     # Exact match for the original input
        )
        print(f"Filtered Queryset: {filtered_queryset}")  # Debugging line
        
        return filtered_queryset
    
class StockFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label='Search')
    product__category = django_filters.ModelChoiceFilter(queryset=ProductCategory.objects.all(), label='Category')
    product__usage = django_filters.ModelChoiceFilter(queryset=ProductUsage.objects.all(), label='Usage')

    class Meta:
        model = Stock
        fields = ['product__name', 'product__category', 'product__usage']

    def filter_by_all(self, queryset, name, value):
        if not value:
            return queryset
        value = value.strip().lower()
        return queryset.filter(
            Q(product__name__icontains=value) |
            Q(product__category__name__icontains=value) |
            Q(product__usage__name__icontains=value)
        )