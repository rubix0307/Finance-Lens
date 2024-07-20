from django import forms
from .models import Product, ProductCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']

ProductFormSet = forms.modelformset_factory(Product, form=ProductForm, extra=0)