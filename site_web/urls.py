from django.urls import path
from .views import AboutView, ServicesView, ContactView

urlpatterns = [
    
    path('a-propos/', AboutView.as_view(), name='about'),
    path('nos-services/', ServicesView.as_view(), name='services'),
    path('contact/', ContactView.as_view(), name='contact'),

]