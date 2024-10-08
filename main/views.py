import datetime
from urllib.parse import urlencode

from django.contrib.auth import login
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from user.models import CustomUser
from .models import Receipt, Section
from .forms import ProductFormSet, SectionCurrencyForm
from .services.section_service import SectionService
from .statistic import get_section_statistic


def permission_denied_view(request):
    return render(request, '403.html', status=403)


@login_required
def get_section_stats(request):
    section = get_object_or_404(Section, id=request.GET.get('id'), sectionuser__user=request.user)
    currency = section.get_user_currency(request.user)
    stats = get_section_statistic(
        section,
        currency,
        month=request.GET.get('month'),
        year=request.GET.get('year'),
    )
    return JsonResponse(stats, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


@login_required
def index(request):
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
            return render(request, 'main/receipts/receipt.html', context={'receipt': receipt, 'is_updated': True})
    else:
        section, *_ = SectionService.get_or_create_base_section_by_user(request.user)
        url = reverse('section')
        params = {
            'id': section.id,
        }
        return redirect(f'{url}?{urlencode(params)}')


@login_required
def show_section(request):
    section = get_object_or_404(Section, id=request.GET.get('id'), sectionuser__user=request.user)
    currency_form = SectionCurrencyForm(
        initial_currency=section.get_user_currency(request.user),
        currency_label='Валюта секции',
    )
    context = {
        'section': section,
        'user_sections': request.user.sections.all(),
        'currency_form': currency_form,
    }
    return render(request, 'main/index.html', context=context)


@login_required
def show_feed(request):
    section = get_object_or_404(Section, id=request.GET.get('id'), sectionuser__user=request.user)
    receipts = Receipt.objects.filter(section=section).order_by('-date', '-id').prefetch_related('products')[:100]

    for receipt in receipts:
        receipt.formset = ProductFormSet(queryset=receipt.products.all())

    context = {
        'section': section,
        'receipts': receipts,
    }
    return render(request, 'main/receipts/index.html', context=context)



@login_required
def change_currency(request):
    section = get_object_or_404(
        Section,
        id=request.GET.get('id'),
        sectionuser__user=request.user,
        sectionuser__is_owner=True,
    )

    if request.method == 'POST':
        form = SectionCurrencyForm(request.POST)
        is_valid = form.is_valid()
        new_currency = form.cleaned_data.get('currency')

        if is_valid and new_currency:
            section.set_user_currency(user=request.user, currency=new_currency)
            messages.success(request, f'Валюта успешно обновлена')
        else:
            messages.error(request, 'Валюта не была обновлена')

        url = reverse('section')
        params = {
            'id': section.id,
        }
        return redirect(f'{url}?{urlencode(params)}')

    messages.error(request, 'Запрос на обновление валюты был отклонен')
    return redirect('index')


@login_required
def delete_receipt(request, receipt_id):
    if request.method == 'POST':
        receipt = get_object_or_404(Receipt, id=receipt_id)
        receipt.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
