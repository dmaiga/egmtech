from django.views.generic import TemplateView
from django.shortcuts import render
from catalog.models import Category
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm
from .models import ContactMessage


class AboutView(TemplateView):
    template_name = "about.html"

class ServicesView(TemplateView):
    template_name = "services.html"

class GalerieView(TemplateView):
    template_name = "galerie.html"


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "contact.html"
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, "Merci ! Votre message a été transmis à nos experts.")
        return super().form_valid(form)


def fibre_optique(request):
    return render(request, 'services/fibre_optique.html')

def securite_electronique(request):
    return render(request, 'services/securite_electronique.html')

def energie_solaire(request):
    return render(request, 'services/energie.html')

def reseau_informatique(request):
    return render(request, 'services/reseau_informatique.html')

def maintenance_informatique(request):
    return render(request, 'services/maintenance_informatique.html')

def formation(request):
    return render(request, 'services/formation.html')


