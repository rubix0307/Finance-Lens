from django.shortcuts import render

from main.models import Product

from django.shortcuts import render, redirect
from .models import Product, ProductCategory
from .forms import ProductFormSet


def index(request):
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        is_valid = formset.is_valid()
        print(f'{is_valid=}')
        if is_valid:
            formset.save()
    else:
        queryset = Product.objects.all()
        formset = ProductFormSet(queryset=queryset)

    return render(request, 'main/index.html', {'formset': formset})
