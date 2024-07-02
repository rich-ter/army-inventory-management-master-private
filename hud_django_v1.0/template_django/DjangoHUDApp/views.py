from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.http import HttpResponse  # Add this import
from .forms import ProductForm, ShipmentForm, ShipmentItemFormSet
from .models import Product, Shipment, Warehouse, Recipient, ShipmentItem, Stock, ProductCategory, ProductUsage  
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F, Q
from django.contrib.auth.decorators import login_required
from .filters import ProductFilter, ShipmentFilter, RecipientFilter, StockFilter
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import ProductCategory, ProductUsage
from django.urls import reverse
from django.db.models import Q
from datetime import timedelta
from django.db.models import Sum, Max


# Function for loging a user 
def pageLogin(request):
    if request.method == 'GET':
        form = LoginForm()
    else:  # POST request
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('DjangoHUDApp:index')  # Make sure 'dashboard' is a valid named route in your urls.py
            else:
                # For debugging: Return a simple response indicating failure
                return HttpResponse("Invalid login attempt", status=401)
        else:
            # For debugging: Indicate form is not valid
            return HttpResponse("Form is not valid", status=400)
    
    context = {
        "form": form,
        "appSidebarHide": 1,
        "appHeaderHide": 1,
        "appContentClass": 'p-0'
    }
    return render(request, "pages/login.html", context)

def logout_view(request):
     logout(request)
     return redirect('DjangoHUDApp:pageLogin')

# Function for creating a product 
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            product.owners.set(request.user.groups.all())  # Assign the product to the user's groups
            product.save()
            return redirect('DjangoHUDApp:pageProduct')  # Redirect to an appropriate page after saving
        else:
            return render(request, 'pages/add_product.html', {
                'form': form,
                'product_category_choices': Product.PRODUCT_CATEGORY,
                'product_usage_choices': Product.PRODUCT_USAGE,
                'unit_of_measurement_choices': Product.MEASUREMENT_TYPES,
            })
    else:
        form = ProductForm()
        context = {
            'form': form,
            'product_category_choices': ProductCategory.objects.all(),
            'product_usage_choices': ProductUsage.objects.all(),
            'unit_of_measurement_choices': Product.MEASUREMENT_TYPES,
        }
        return render(request, 'pages/add_product.html', context)
    
    
@login_required
def pageProduct(request):
    user_groups = request.user.groups.all()
    if request.user.is_superuser:
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(owners__in=user_groups).distinct()

    product_filter = ProductFilter(request.GET, queryset=products_list)
    products_list = product_filter.qs

    paginator = Paginator(products_list, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {'products': products, 'filter': product_filter}
    return render(request, "pages/all-products.html", context)



@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Shipment deleted successfully.')
    return redirect(reverse('DjangoHUDApp:pageProduct'))


# Function for individual product details
@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('DjangoHUDApp:pageProduct')  # Redirect to an appropriate page after updating
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'product_category_choices': Product.category,
        'product_usage_choices': Product.usage,
        'unit_of_measurement_choices': Product.MEASUREMENT_TYPES,
    }
    return render(request, 'pages/product-details.html', context)


@login_required
def add_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST, request.FILES)
        formset = ShipmentItemFormSet(request.POST, prefix='shipmentitem', user=request.user)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    shipment = form.save(commit=False)
                    shipment.user = request.user
                    shipment.date = timezone.now()
                    shipment.save()

                    formset.instance = shipment
                    formset.save()

                    return redirect('DjangoHUDApp:pageOrder')
            except ValidationError as e:
                form.add_error(None, e)
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = ShipmentForm()
        formset = ShipmentItemFormSet(prefix='shipmentitem', user=request.user)

    return render(request, 'pages/add_order.html', {'form': form, 'formset': formset})


@login_required
def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.delete()
    messages.success(request, 'Shipment deleted successfully.')
    return redirect(reverse('DjangoHUDApp:pageOrder'))

@login_required
def pageOrder(request):
    user = request.user

    # Admin users see all shipments
    if user.is_superuser:
        shipments_list = Shipment.objects.all()
    else:
        # Filter shipments by the groups of the user
        user_groups = user.groups.values_list('name', flat=True)
        if 'ΔΙΔΕΣ' in user_groups:
            # Users in ΔΙΔΕΣ see shipments from all users in this group
            shipments_list = Shipment.objects.filter(user__groups__name='ΔΙΔΕΣ')
        elif 'ΔΟΡΥΦΟΡΙΚΑ' in user_groups:
            # Users in ΔΟΡΥΦΟΡΙΚΑ only see their own shipments
            shipments_list = Shipment.objects.filter(user=user)
        else:
            # Default to no shipments if no specific group is found
            shipments_list = Shipment.objects.none()

    # Apply the filter
    shipments_filter = ShipmentFilter(request.GET, queryset=shipments_list)
    shipments_list = shipments_filter.qs

    # Sort by most recent date
    shipments_list = shipments_list.order_by('-date')

    # Paginate the results
    paginator = Paginator(shipments_list, 10)  # Show 10 shipments per page
    page_number = request.GET.get('page')
    shipments = paginator.get_page(page_number)

    context = {
        'shipments': shipments,
        'filter': shipments_filter,
    }
    return render(request, "pages/all-orders.html", context)

    
@login_required
def pageWarehouse(request):
    user_groups = request.user.groups.values_list('name', flat=True)

    if request.user.is_superuser or 'Admin' in user_groups:
        warehouses_list = Warehouse.objects.annotate(
            total_stock=Sum('stocks__quantity'),
            last_shipment_date=Max('shipmentitem__shipment__date')
        )
    elif 'ΔΟΡΥΦΟΡΙΚΑ' in user_groups:
        warehouses_list = Warehouse.objects.filter(name="ΔΟΡΥΦΟΡΙΚΑ").annotate(
            total_stock=Sum('stocks__quantity'),
            last_shipment_date=Max('shipmentitem__shipment__date')
        )
    elif 'ΔΙΔΕΣ' in user_groups:
        warehouses_list = Warehouse.objects.filter(name__in=["ΚΕΠΙΚ", "ΤΑΓΜΑ"]).annotate(
            total_stock=Sum('stocks__quantity'),
            last_shipment_date=Max('shipmentitem__shipment__date')
        )
    else:
        warehouses_list = Warehouse.objects.none()

    context = {'warehouses': warehouses_list}
    return render(request, "pages/warehouses.html", context)

@login_required
def pageDataManagement(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = file.name

        if file_name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(file, header=0)
        else:
            return HttpResponse("Unsupported file format", status=400)

        # Strip whitespace from column names to avoid KeyError
        df.columns = df.columns.str.strip()

        # Print columns for debugging after stripping
        print("DataFrame columns after stripping:", df.columns)

        # Fill NaN values with empty strings to avoid errors
        df.fillna('', inplace=True)

        # Check for required columns and print a warning if any are missing
        required_columns = ['Προιόν', 'Κατηγορία', 'Χρήση', 'Μερίδα', 'Απ. ΤΑΓΜΑ', 'Απ. ΚΕΠΙΚ', 'Απ. ΔΟΡΥΦΟΡΙΚΑ']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return HttpResponse(f"Missing columns in the uploaded file: {', '.join(missing_columns)}", status=400)

        # Process the DataFrame to update Products and Stocks
        for index, row in df.iterrows():
            product_name = str(row['Προιόν']).strip()
            category_name = str(row['Κατηγορία']).strip()
            usage_name = str(row['Χρήση']).strip()
            batch_number = str(row['Μερίδα']).strip()
            # total_stock = row['Συνολικό Απόθεμα']
            stock_tagma = row['Απ. ΤΑΓΜΑ']
            stock_kepik = row['Απ. ΚΕΠΙΚ']
            stock_doriforika = row['Απ. ΔΟΡΥΦΟΡΙΚΑ']

            category, _ = ProductCategory.objects.get_or_create(name=category_name)
            usage, _ = ProductUsage.objects.get_or_create(name=usage_name)

            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={'category': category, 'usage': usage, 'batch_number': batch_number}
            )

            if not created:
                product.category = category
                product.usage = usage
                product.batch_number = batch_number
                product.save()

            warehouses = {
                'ΤΑΓΜΑ': stock_tagma,
                'ΚΕΠΙΚ': stock_kepik,
                'ΔΟΡΥΦΟΡΙΚΑ': stock_doriforika
            }

            for warehouse_name, quantity in warehouses.items():
                warehouse, _ = Warehouse.objects.get_or_create(name=warehouse_name)
                stock, _ = Stock.objects.get_or_create(product=product, warehouse=warehouse)
                stock.quantity = quantity
                stock.save()

        return redirect('DjangoHUDApp:pageDataManagement')

    user = request.user
    products = Product.objects.none()
    warehouse_filter = []

    if user.is_superuser:
        products = Product.objects.annotate(total_stock=Sum('stocks__quantity'))
        warehouse_filter = ['ΚΕΠΙΚ', 'ΔΟΡΥΦΟΡΙΚΑ', 'ΤΑΓΜΑ']
    else:
        user_groups = user.groups.values_list('name', flat=True)
        if 'ΔΙΔΕΣ' in user_groups:
            products = Product.objects.filter(owners__name='ΔΙΔΕΣ').annotate(total_stock=Sum('stocks__quantity'))
            warehouse_filter = ['ΚΕΠΙΚ', 'ΤΑΓΜΑ']
        elif 'ΔΟΡΥΦΟΡΙΚΑ' in user_groups:
            products = Product.objects.filter(owners__name='ΔΟΡΥΦΟΡΙΚΑ').annotate(total_stock=Sum('stocks__quantity'))
            warehouse_filter = ['ΔΟΡΥΦΟΡΙΚΑ']

    warehouses = Warehouse.objects.filter(name__in=warehouse_filter)
    warehouse_dict = {wh.name: wh for wh in warehouses}

    for product in products:
        product.stock_kepik = product.stock_doriforika = product.stock_tagma = 0
        stocks = Stock.objects.filter(product=product, warehouse__in=warehouses)
        for stock in stocks:
            if stock.warehouse.name == 'ΚΕΠΙΚ':
                product.stock_kepik = stock.quantity
            elif stock.warehouse.name == 'ΔΟΡΥΦΟΡΙΚΑ':
                product.stock_doriforika = stock.quantity
            elif stock.warehouse.name == 'ΤΑΓΜΑ':
                product.stock_tagma = stock.quantity

    context = {
        'appContentFullHeight': 1,
        'appContentClass': 'py-3',
        'products_with_stock': products,
        'can_view_kepik': 'ΚΕΠΙΚ' in warehouse_filter,
        'can_view_doriforika': 'ΔΟΡΥΦΟΡΙΚΑ' in warehouse_filter,
        'can_view_tagma': 'ΤΑΓΜΑ' in warehouse_filter,
    }

    return render(request, 'pages/all-stock.html', context)

@login_required
def stockPerWarehouse(request, warehouse_name):
    warehouse = get_object_or_404(Warehouse, name=warehouse_name)
    stock_list = Stock.objects.filter(warehouse=warehouse).select_related('product')
    
    stock_filter = StockFilter(request.GET, queryset=stock_list)
    stock_list = stock_filter.qs

    context = {
        'warehouse': warehouse,
        'stock_items': stock_list,
        'filter': stock_filter
    }

    return render(request, "pages/stock-per-warehouse.html", context)


@login_required
def pageRecipient(request):
    recipients_list = Recipient.objects.all()

    # Apply filtering
    recipients_filter = RecipientFilter(request.GET, queryset=recipients_list)
    recipients_list = recipients_filter.qs

    # Paginate the filtered recipients

    context = {
        'recipients': recipients_list,
        'filter': recipients_filter,
    }
    return render(request, "pages/recipients.html", context)


# def index(request):
# 	return render(request, "pages/index.html")

@login_required
def index(request):
    user = request.user

    # Get the user's groups
    user_groups = user.groups.all()

    # Calculate the total number of products the user can view in their warehouses
    total_products = Product.objects.filter(owners__in=user_groups).distinct().count()
    total_shipments_sent = Shipment.objects.filter(user=user).count()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    shipments = Shipment.objects.all()
    stocks = Stock.objects.all()

    top_products = (Stock.objects
                    .filter(warehouse__access_groups__in=user_groups)
                    .select_related('product__category', 'product__usage')
                    .annotate(
                        product_name=F('product__name'),
                        product_image_url=F('product__image'),
                        product_category_name=F('product__category__name'),
                        product_batch_number=F('product__batch_number'),
                        product_unit_of_measurement=F('product__unit_of_measurement'),
                        product_usage_name=F('product__usage__name'),
                        total_quantity=Sum('quantity')
                    )
                    .values(
                        'product_name', 
                        'product_image_url', 
                        'product_category_name', 
                        'product_batch_number', 
                        'product_unit_of_measurement', 
                        'product_usage_name',
                        'total_quantity'
                    )
                    .order_by('-total_quantity')[:10])

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        if start_date and end_date:
            # Adjust the end_date to include the whole day
            end_date += timedelta(days=1)
            shipments = shipments.filter(date__range=[start_date, end_date])
        total_shipments = shipments.count()
    else:
        total_shipments = shipments.count()

    # Calculate total stock
    total_stock = stocks.aggregate(total_quantity=Sum('quantity'))['total_quantity']

    if user.is_superuser:
        # Admin can view all recent shipments
        recent_shipments = shipments.order_by('-date')[:10]
    else:
        # Non-admin users only see shipments related to their groups
        recent_shipments = shipments.filter(
            Q(user__groups__in=user_groups)
        ).distinct().order_by('-date')[:10]

    context = {
        'top_products': top_products,
        'total_products': total_products,
        'total_shipments_sent': total_shipments_sent,
        'start_date': start_date,
        'end_date': end_date,
        'total_shipments': total_shipments,
        'total_stock': total_stock,
        'recent_shipments': recent_shipments,
    }
    return render(request, 'pages/index.html', context)

def pageOrderDetails(request, shipment_id):
    shipment = get_object_or_404(Shipment, pk=shipment_id)
    shipment_items = ShipmentItem.objects.filter(shipment=shipment)
    return render(request, "pages/page-order-details.html", {"shipment": shipment, "shipment_items": shipment_items})


# def pageOrderDetails(request, shipment_id):  # Accept shipment_id as a parameter
#     shipment = get_object_or_404(Shipment, pk=shipment_id)
#     # shipment_items = ShipmentItem.objects.filter(shipment=shipment)
#     return render(request, "pages/page-order-details.html", {'shipment': shipment})



def order_print(request, shipment_id):
    shipment = get_object_or_404(Shipment, pk=shipment_id)
    shipment_items = ShipmentItem.objects.filter(shipment=shipment)

    # Get the creator's group
    creator_group = shipment.user.groups.first().name if shipment.user.groups.exists() else None

    return render(request, "doriforika-protokolo.html", {
        "shipment": shipment,
        "shipment_items": shipment_items,
        "creator_group": creator_group,
    })








# # # # # # # # # # # # ANALYTICS PAGES # # # # # # # # # # # # 

def analytics(request):
	return render(request, "pages/analytics.html")


def chartJs(request):
	return render(request, "pages/chart-js.html")

def chartApex(request):
	return render(request, "pages/chart-apex.html")



# # # # # # # # # # # # 404 PAGES # # # # # # # # # # # # 


def pageError(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)

	
def error404(request):
	context = {
		"appSidebarHide": 1,
		"appHeaderHide": 1,
		"appContentClass": 'p-0'
	}
	return render(request, "pages/page-error.html", context)


def handler404(request, exception):
    context = {
        "appSidebarHide": 1,
        "appHeaderHide": 1,
        "appContentClass": 'p-0'
    }
    return render(request, 'pages/page-error.html', context, status=404)