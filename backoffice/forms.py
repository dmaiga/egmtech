from django import forms
from catalog.models import Product, Category
from orders.models import QuoteRequest


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full focus:border-egmblue rounded-xl font-medium',
                'placeholder': 'Ex: Équipements de Sécurité'
            }),
            'image': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered file-input-primary w-full rounded-xl',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary shadow-sm'
            }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'brand', 'price', 'stock', 
            'image', 'datasheet', 'description', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl font-medium', 'placeholder': 'Nom de l\'équipement'}),
            'brand': forms.TextInput(attrs={'class': 'input input-bordered w-full rounded-xl', 'placeholder': 'Marque (ex: Hikvision, Cisco...)'}),
            'category': forms.Select(attrs={'class': 'select select-bordered w-full rounded-xl font-bold text-egmblue'}),
            'price': forms.NumberInput(attrs={'class': 'input input-bordered w-full rounded-xl font-bold', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'input input-bordered w-full rounded-xl'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full rounded-xl', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'file-input file-input-bordered file-input-primary w-full rounded-xl'}),
            'datasheet': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full rounded-xl'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary shadow-sm'}),
        }



class QuoteResponseForm(forms.ModelForm):

    class Meta:
        model = QuoteRequest
        fields = ["admin_response", "proforma_file"]

        widgets = {
            "admin_response": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full rounded-xl",
                "rows": 5,
                "placeholder": "Réponse commerciale..."
            }),

            "proforma_file": forms.FileInput(attrs={
                "class": "file-input file-input-bordered w-full rounded-xl"
            }),


        }