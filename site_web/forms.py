from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-egmblue',
                'placeholder': 'Ex: Zan Traoré'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-egmblue',
                'placeholder': 'Ex: +223 XX XX XX X'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-egmblue',
                'placeholder': 'contact@entreprise.ml'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'input input-bordered rounded-xl bg-slate-50 border-none focus:ring-2 focus:ring-egmblue',
                'placeholder': 'Objet de votre demande'
            }),
            'message': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered rounded-xl bg-slate-50 border-none h-32',
                'placeholder': 'Décrivez votre besoin technique...'
            }),
        }