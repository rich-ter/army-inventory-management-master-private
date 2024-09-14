# forms.py
from django import forms
from .models import Product, Shipment, ShipmentItem, Warehouse
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from .models import Product, ProductCategory, ProductUsage
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-inverse bg-opacity-5', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg bg-inverse bg-opacity-5', 'placeholder': 'Password'})
    )

class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Όνομα Υλικού'}))
    batch_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Αριθμός Μερίδας Υλικού'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}), required=False)
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

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['shipment_type', 'recipient', 'signatory', 'date', 'order_number', 'notes', 'attachment']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Select a date and time', 'type': 'text'}),
            'shipment_type': forms.Select(attrs={'class': 'form-select', 'id': 'shipment_type_id'}),
            'recipient': forms.Select(attrs={'class': 'form-select', 'id': 'recipient_id'}),
            'signatory': forms.TextInput(attrs={'class': 'form-control', 'id': 'signatory_id'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'order_number_id'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'})  # Add this line for file input
        }
        labels = {
            'shipment_type': 'Τύπος Αποστολής',  # Custom title for shipment_type
            'recipient': 'Παραλήπτης (OUT) / Αποστολέας (IN)',  # Custom title for recipient
            'signatory': 'Υπογεγραμμένος',  # Custom title for recipient
            'date': 'Ημερομηνία',  # Custom title for date
            'order_number': 'Αριθμός Διαταγής',
            'notes': 'Σημειώσεις',  # Custom title for notes
            'attachment': 'Συνημμένο'  # Custom title for attachment
        }

    date = forms.DateField(input_formats=['%d-%m-%Y'], widget=forms.DateInput(attrs={
        'class': 'form-control', 'placeholder': 'Select a date', 'type': 'text', 'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super(ShipmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().strftime('%d-%m-%Y')

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
                self.fields['product'].queryset = Product.objects.all().order_by('name')
                self.fields['warehouse'].queryset = Warehouse.objects.all()
            else:
                user_groups = user.groups.all()
                self.fields['product'].queryset = Product.objects.filter(owners__in=user_groups).distinct().order_by('name')
                self.fields['warehouse'].queryset = Warehouse.objects.filter(access_groups__in=user_groups).distinct()
        self.fields['product'].widget.attrs.update({'class': 'form-select mb-2'})
        self.fields['warehouse'].widget.attrs.update({'class': 'form-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ποσότητα'})

class ShipmentItemFormSetWithUser(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from the keyword arguments
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if self.user.is_superuser:
                form.fields['product'].queryset = Product.objects.all().order_by('name')
                form.fields['warehouse'].queryset = Warehouse.objects.all()
            else:
                user_groups = self.user.groups.all()
                form.fields['product'].queryset = Product.objects.filter(owners__in=user_groups).distinct().order_by('name')
                form.fields['warehouse'].queryset = Warehouse.objects.filter(access_groups__in=user_groups).distinct()

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            raise forms.ValidationError('You must add at least one shipment item.')

ShipmentItemFormSet = inlineformset_factory(
    Shipment,
    ShipmentItem,
    form=ShipmentItemForm,  # Use the customized form
    formset=ShipmentItemFormSetWithUser,
    fields=('product', 'warehouse', 'quantity'),
    extra=1,
    can_delete=True
)
