from django.urls import path
from . import views

urlpatterns = [
    path("buy/<slug:product_slug>/", views.buy_product, name="buy_product"),
    path("devis/", views.request_quote, name="request_quote"),
    path("order/success/", views.order_success, name="order_success"),
    # Panier
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('panier/supprimer/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # Commande
    path('validation/', views.checkout, name='checkout'),
    path('confirmation/', views.order_success, name='order_success'),
   ]