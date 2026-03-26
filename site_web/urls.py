from django.urls import path
from .views import *

urlpatterns = [
    
    path('a-propos/', AboutView.as_view(), name='about'),
    path('nos-services/', ServicesView.as_view(), name='services'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/fibre-optique/', fibre_optique, name='fibre_optique'),
    path('services/securite-electronique/', securite_electronique, name='securite_electronique'),
    path('services/energie-solaire/', energie_solaire, name='energie_solaire'),
    path('services/reseau-informatique/', reseau_informatique, name='reseau_informatique'),
    path('services/maintenance-informatique/', maintenance_informatique, name='maintenance_informatique'),
    path('services/formation/', formation, name='formation'),
    path('galerie/', GalerieView.as_view(), name='galerie'),
]