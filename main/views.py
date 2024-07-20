from django.shortcuts import render, redirect
from .models import Product, Receipt
from .forms import ProductFormSet


def index(request):
    context = {}

    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        is_valid = formset.is_valid()
        print(f'{is_valid=}')
        if is_valid:
            formset.save()
            return redirect('index')
    else:
        receipt = Receipt.objects.last()
        products = receipt.products.all()
        formset = ProductFormSet(queryset=products)
        context['receipt'] = receipt

    context['formset'] = formset

    return render(request, 'main/index.html', context=context)
