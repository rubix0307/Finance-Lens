from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Receipt
from .forms import ProductFormSet
from .statistic import get_monthly_expenses


def permission_denied_view(request):
    return render(request, '403.html', status=403)


@login_required
def index(request):
    monthly_expenses = get_monthly_expenses(request.user)
    context = {'monthly_expenses':monthly_expenses}

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
        receipts = Receipt.objects.filter(owner=request.user).order_by('-date', '-id').prefetch_related('products')[:100]

        for receipt in receipts:
            receipt.formset = ProductFormSet(queryset=receipt.products.all())
        context['receipts'] = receipts

    return render(request, 'main/index.html', context=context)
