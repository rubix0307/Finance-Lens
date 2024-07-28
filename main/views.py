import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Receipt
from .forms import ProductFormSet
from .statistic import get_monthly_expenses


def permission_denied_view(request):
    return render(request, '403.html', status=403)


@login_required
def index(request):
    context = {}

    if request.method == 'POST':

        formset = ProductFormSet(request.POST)
        is_valid = formset.is_valid()
        print(f'{is_valid=}')
        if is_valid:

            for form in formset:
                instance = form.save(commit=False)
                instance.save()

            receipt = formset.cleaned_data[0]['id'].receipt
            receipt.formset = formset
            return render(request, 'main/receipt/index.html', context={'receipt': receipt, 'is_updated': True})
    else:

        monthly_expenses = get_monthly_expenses(request.user)
        receipts = Receipt.objects.filter(owner=request.user).order_by('-date', '-id').prefetch_related('products')[:100]

        for receipt in receipts:
            receipt.formset = ProductFormSet(queryset=receipt.products.all())

        context['receipts'] = receipts
        context['monthly_expenses'] = monthly_expenses

    return render(request, 'main/index.html', context=context)

@login_required
def delete_receipt(request, receipt_id):
    if request.method == 'POST':
        receipt = get_object_or_404(Receipt, id=receipt_id)
        receipt.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)