from django import forms

from django import forms
from catalog.models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','is_active']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'brand',
            'price',
            'stock',
            'image',
            'datasheet',
            'description',
            'is_active',
            'promo_percent',
            'promo_active'
        ]