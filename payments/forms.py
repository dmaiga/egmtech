from django import forms
from payments.models import Payment

class DirectPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["product_direct", "quantity_direct", "amount", "method", "reference"]
        widgets = {
            "product_direct": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "quantity_direct": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": "1"}),
            "amount": forms.NumberInput(attrs={"class": "input input-bordered w-full", "placeholder": "Montant"}),
            "method": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "reference": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Référence (ex: N° Reçu)"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.payment_type = "DIRECT" # On force le type
        instance.order = None
        instance.quote = None
        if commit:
            instance.save()
        return instance
    
class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "method", "reference"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "input input-bordered w-full"}),
            "method": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "reference": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "ID Transaction"}),
        }

    def save(self, order, user, commit=True):
        instance = super().save(commit=False)
        instance.payment_type = "ORDER"
        instance.order = order
        instance.received_by = user
        if commit:
            instance.save()
        return instance
    

class QuotePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "method", "reference"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "input input-bordered w-full"}),
            "method": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "reference": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
        }

    def save(self, quote, user, commit=True):
        instance = super().save(commit=False)
        instance.payment_type = "QUOTE"
        instance.quote = quote
        instance.received_by = user
        if commit:
            instance.save()
        return instance