from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    
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

]