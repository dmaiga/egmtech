from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    #CLIENTS
    path("customers/", views.customer_list, name="customer_list"),
    path('customers/create/', views.customer_create, name='customer_create'),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    
    # Produits
    path("products/", views.product_list, name="bo_product_list"),
    path("products/create/", views.product_create, name="bo_product_create"),
    path("products/<int:pk>/", views.product_detail, name="bo_product_detail"),
    path("products/<int:pk>/edit/", views.product_update, name="bo_product_update"),
    path("products/<int:pk>/toggle/", views.product_toggle_active, name="bo_product_toggle"),
    path("products/<int:pk>/delete/", views.product_delete, name="bo_product_delete"),

    # Catégories
    path("categories/", views.category_list, name="bo_category_list"),
    path("categories/create/", views.category_create, name="bo_category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="bo_category_update"),
    path("categories/<int:pk>/toggle/", views.category_toggle_active, name="bo_category_toggle"),

    # ===== ORDERS =====
    path("orders/", views.bo_order_list, name="bo_order_list"),
    path("orders/<int:pk>/", views.bo_order_detail, name="bo_order_detail"),
    path("orders/<int:pk>/update-status/", views.bo_order_update_status, name="bo_order_update_status"),
    # ===== QUOTE =====
    path('devis/', views.quote_list, name='bo_quote_list'),
    path('devis/<int:pk>/', views.quote_detail, name='bo_quote_detail'),

    # ===== PAYMENT =====
    path("payment/", views.payment_list, name="payment_list"),
    path("payment/<int:pk>/", views.payment_detail, name="payment_detail"),
    path('payment/<int:pk>/cancel/', views.payment_cancel, name='payment_cancel'),

    path("payment/create/", views.direct_payment_create, name="direct_payment_create"),
    path('payment/orders/<int:pk>/add-payment/', views.order_add_payment, name='order_add_payment'),
   
    path('payment/quotes/<int:pk>/add-payment/', views.quote_add_payment, name='quote_add_payment'),
    path('payment/quotes/<int:pk>/close/', views.quote_close_deal, name='quote_close_deal'),


]