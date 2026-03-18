# orders/forms
from django import forms
from .models import Order,QuoteRequest





class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

class CartAddProductForm(forms.Form):

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'bg-transparent border-none w-16 text-center font-black text-slate-800 focus:ring-0',
        })
    )
    # override est utile pour savoir si on ajoute à l'existant ou si on remplace
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
 

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["subject", "description", "attachment"]

        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "input input-bordered w-full pl-10 focus:border-egmblue rounded-xl bg-slate-50",
                "placeholder": "Ex: Installation de 4 caméras IP pour entrepôt"
            }),
            "description": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full focus:border-egmblue rounded-xl bg-slate-50",
                "rows": 5,
                "placeholder": "Décrivez votre besoin : distance des câbles, stockage souhaité, type de bâtiment..."
            }),
            "attachment": forms.FileInput(attrs={
                "class": "file-input file-input-bordered w-full focus:border-egmblue rounded-xl bg-slate-50 text-sm"
            }),
        }