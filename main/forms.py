from django import forms
from .models import Product, ProductCategory, Currency


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']


ProductFormSet = forms.modelformset_factory(Product, form=ProductForm, extra=0)


class SectionCurrencyForm(forms.Form):
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.order_by('code'),
        required=True,
        widget=forms.Select(attrs={'class': 'default-tg-border'})
    )

    def __init__(self, *args, **kwargs):
        initial_currency = kwargs.pop('initial_currency', None)
        currency_label = kwargs.pop('currency_label', None)

        super(SectionCurrencyForm, self).__init__(*args, **kwargs)

        if initial_currency:
            self.fields['currency'].initial = initial_currency

        if currency_label:
            self.fields['currency'].label = currency_label
