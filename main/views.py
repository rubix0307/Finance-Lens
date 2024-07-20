from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductFormSet


def index(request):
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        is_valid = formset.is_valid()
        print(f'{is_valid=}')
        if is_valid:
            formset.save()
            return redirect('index')
    else:
        queryset = Product.objects.all()
        formset = ProductFormSet(queryset=queryset)

    return render(request, 'main/index.html', {'formset': formset})
