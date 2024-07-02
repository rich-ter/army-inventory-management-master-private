from django.urls import path
from . import views

app_name = 'DjangoHUDApp'
urlpatterns = [
    # in use
    
    #general pages
    path('', views.pageLogin, name='pageLogin'),
    path('index', views.index, name='index'),
    path('404/', views.error404, name='error404'),
    path('page/error', views.pageError, name='pageError'),  
    path('logout/', views.logout_view, name='logout'),

    #product pages
    path('all-products', views.pageProduct, name='pageProduct'),
    path('add-product', views.add_product, name='add_product'),
    path('product-details/<int:product_id>/', views.product_details, name='pageProductDetails'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    #order pages
    path('add-shipment', views.add_shipment, name='add_shipment'),
    path('order', views.pageOrder, name='pageOrder'),
    path('order-details/<int:shipment_id>/', views.pageOrderDetails, name='pageOrderDetails'),
    path('order-details/<int:shipment_id>/print/', views.order_print, name='order_print'),
    path('delete-shipment/<int:shipment_id>/', views.delete_shipment, name='delete_shipment'),
    
    #warehouse pages
    path('warehouse', views.pageWarehouse, name='pageWarehouse'),
    path('stock-per-warehouse/<str:warehouse_name>/', views.stockPerWarehouse, name='pageStockPerWarehouse'),

    #stock pages
    path('stock', views.pageDataManagement, name='pageDataManagement'),

    #recipient pages
    path('recipient', views.pageRecipient, name='pageRecipient'),

    # not in use
    path('analytics/', views.analytics, name='  '),
    path('chart/js/', views.chartJs, name='chartJs'),
    path('chart/apex/', views.chartApex, name='chartApex'),
]

handler404 = 'DjangoHUDApp.views.handler404'
