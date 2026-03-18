from django import forms
from django.contrib.auth import get_user_model
from django import forms
 
 
from django.utils.text import slugify

User = get_user_model()

 

class ClientProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'email@exemple.com'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': '+223 ...'}),
            'avatar': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full rounded-xl'}),
        }


class AdminCustomerCreationForm(forms.ModelForm):
    send_welcome_email = forms.BooleanField(required=False, initial=True, label="Envoyer les accès par email")

    class Meta:
        model = User
        # On retire 'username' de la saisie
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'email@exemple.com'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': '+223 ...'}),
            'avatar': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full rounded-xl'}),
            'role': forms.Select(attrs={'class': 'select select-bordered w-full rounded-xl'}),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if not data:
            raise forms.ValidationError("Le prénom est requis pour générer l'identifiant.")
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        if not data:
            raise forms.ValidationError("Le nom est requis pour générer l'identifiant.")
        return data