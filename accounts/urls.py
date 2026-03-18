from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("client/", views.dashboard_client, name="dashboard_client"),
    path("client/orders/", views.client_orders, name="client_orders"),
    path("client/quotes/", views.client_quotes, name="client_quotes"),

    path("client/quotes/<int:id>", views.quote_detail, name="quote_detail"),
    
    path("client/profile/", views.client_profile, name="client_profile"),
    path('profile/edit/', views.client_profile_edit, name='client_profile_edit'),
    path('profile/password/', views.password_change_custom, name='password_change'),
]