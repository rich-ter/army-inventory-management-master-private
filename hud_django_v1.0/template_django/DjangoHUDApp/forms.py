from django import forms
from .models import Product, Shipment, ShipmentItem, Warehouse
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from .models import Product, ProductCategory, ProductUsage

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-inverse bg-opacity-5', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg bg-inverse bg-opacity-5', 'placeholder': 'Password'})
    )


class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Onoma'}))
    batch_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Merida ilikou'}), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 6}), required=False)
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    usage = forms.ModelChoiceField(queryset=ProductUsage.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    unit_of_measurement = forms.ChoiceField(choices=Product.MEASUREMENT_TYPES, widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))  # Adding the image field

    class Meta:
        model = Product
        fields = ['name', 'batch_number', 'category', 'usage', 'description', 'unit_of_measurement', 'image']
        labels = {
            'name': 'Όνομα Προϊόντος',
            'batch_number': 'Αριθμός Μερίδας',
            'category': 'Κατηγορία Προϊόντος',
            'usage': 'Χρήση Προϊόντος',
            'description': 'Περιγραφή',
            'unit_of_measurement': 'Μονάδα Μέτρησης',
            'image': 'Εικόνα Προϊόντος'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_groups = user.groups.all()
            self.fields['owners'].queryset = Group.objects.filter(user__in=user_groups).distinct()
# forms.py
class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['shipment_type', 'recipient', 'date',  'notes', 'attachment']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'shipment_type': forms.Select(attrs={'class': 'form-select', 'id': 'shipment_type_id'}),
            'recipient': forms.Select(attrs={'class': 'form-select', 'id': 'recipient_id'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'})  # Add this line for file input
        }
        labels = {
            'shipment_type': 'Τύπος Αποστολής',  # Custom title for shipment_type
            'recipient': 'Παραλήπτης',  # Custom title for recipient
            'date': 'Ημερομηνία',  # Custom title for date
            'notes': 'Σημειώσεις',  # Custom title for notes
            'attachment': 'Συνημμένο'  # Custom title for attachment
        }

    def __init__(self, *args, **kwargs):
        super(ShipmentForm, self).__init__(*args, **kwargs)

class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ['product', 'warehouse', 'quantity']
        labels = {
            'product': 'Προϊόντος',  # Custom title for shipment_type
            'warehouse': 'Αποθήκη',  # Custom title for recipient
            'quantity': 'Ποσότητα'  # Custom title for date
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from the keyword arguments
        super().__init__(*args, **kwargs)
        if user:
            if user.is_superuser:
                self.fields['product'].queryset = Product.objects.all()
                self.fields['warehouse'].queryset = Warehouse.objects.all()
            else:
                user_groups = user.groups.all()
                self.fields['product'].queryset = Product.objects.filter(owners__in=user_groups).distinct()
                self.fields['warehouse'].queryset = Warehouse.objects.filter(access_groups__in=user_groups).distinct()
        self.fields['product'].widget.attrs.update({'class': 'form-select mb-2'})
        self.fields['warehouse'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ποσότητα'})

ShipmentItemFormSet = inlineformset_factory(
    Shipment,
    ShipmentItem,
    form=ShipmentItemForm,
    fields=('product', 'warehouse', 'quantity'),
    extra=1,
    can_delete=True
)

class ShipmentItemFormSetWithUser(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from the keyword arguments
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if self.user.is_superuser:
                form.fields['product'].queryset = Product.objects.all()
                form.fields['warehouse'].queryset = Warehouse.objects.all()
            else:
                user_groups = self.user.groups.all()
                form.fields['product'].queryset = Product.objects.filter(owners__in=user_groups).distinct()
                form.fields['warehouse'].queryset = Warehouse.objects.filter(access_groups__in=user_groups).distinct()
                
ShipmentItemFormSet = inlineformset_factory(
    Shipment,
    ShipmentItem,
    form=ShipmentItemForm,  # Use the customized form
    formset=ShipmentItemFormSetWithUser,
    fields=('product', 'warehouse', 'quantity'),
    extra=1,
    can_delete=True
)