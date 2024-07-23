from django.shortcuts import render, redirect
from django_htmx.middleware import HtmxMiddleware

from .models import Product, Receipt
from .forms import ProductFormSet

def permission_denied_view(request):
    return render(request, '403.html', status=403)

def index(request):
    context = {}

    if request.method == 'POST':

        formset = ProductFormSet(request.POST)
        is_valid = formset.is_valid()
        print(f'{is_valid=}')
        if is_valid:
            formset.save()

            receipt = formset.cleaned_data[0]['id'].receipt
            receipt.formset = formset
            return render(request, 'main/receipt/index.html', context={'receipt': receipt, 'is_updated': True})
    else:
        receipts = Receipt.objects.filter(owner=request.user).order_by('-id').prefetch_related('products')[:100]

        for receipt in receipts:
            receipt.formset = ProductFormSet(queryset=receipt.products.all())
        context['receipts'] = receipts

    return render(request, 'main/index.html', context=context)
