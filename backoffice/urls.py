from django.urls import path
from .views import *
urlpatterns = [
    path("", dashboard_home, name="dashboard_home"),
    #CLIENTS
    path("customers/", customer_list, name="customer_list"),
    path('customers/create/', customer_create, name='customer_create'),
    path("customers/<int:pk>/", customer_detail, name="customer_detail"),
    path('customers/prospects/', AdminContactListView.as_view(), name='admin_contact_list'),
    path('customers/prospects/<int:pk>/', AdminContactDetailView.as_view(), name='admin_contact_detail'),
    # Produits
    path("products/", product_list, name="bo_product_list"),
    path("products/create/", product_create, name="bo_product_create"),
    path("products/<int:pk>/", product_detail, name="bo_product_detail"),
    path("products/<int:pk>/edit/", product_update, name="bo_product_update"),
    path("products/<int:pk>/toggle/", product_toggle_active, name="bo_product_toggle"),
    path("products/<int:pk>/delete/", product_delete, name="bo_product_delete"),

    # Catégories
    path("categories/", category_list, name="bo_category_list"),
    path("categories/create/", category_create, name="bo_category_create"),
    path("categories/<int:pk>/edit/", category_update, name="bo_category_update"),
    path("categories/<int:pk>/toggle/", category_toggle_active, name="bo_category_toggle"),

    # ===== ORDERS =====
    path("orders/", bo_order_list, name="bo_order_list"),
    path("orders/<int:pk>/", bo_order_detail, name="bo_order_detail"),
    path("orders/<int:pk>/update-status/", bo_order_update_status, name="bo_order_update_status"),
    # ===== QUOTE =====
    path('devis/', quote_list, name='bo_quote_list'),
    path('devis/<int:pk>/', quote_detail, name='bo_quote_detail'),

    # ===== PAYMENT =====
    path("payment/", payment_list, name="payment_list"),
    path("payment/<int:pk>/", payment_detail, name="payment_detail"),
    path('payment/<int:pk>/cancel/', payment_cancel, name='payment_cancel'),

    path("payment/create/", direct_payment_create, name="direct_payment_create"),
    path('payment/orders/<int:pk>/add-payment/', order_add_payment, name='order_add_payment'),
   
    path('payment/quotes/<int:pk>/add-payment/', quote_add_payment, name='quote_add_payment'),
    path('payment/quotes/<int:pk>/close/', quote_close_deal, name='quote_close_deal'),


]