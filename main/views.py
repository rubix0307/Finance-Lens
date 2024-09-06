from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Receipt
from .forms import ProductFormSet
from .statistic import get_user_statistic


def permission_denied_view(request):
    return render(request, '403.html', status=403)


@login_required
def get_section_stats(request):
    section = get_object_or_404(Section, id=request.GET.get('id'), sectionuser__user=request.user)
    stats = get_section_statistic(section)
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

    context = {
        'section': section,
        'user_sections': request.user.sections.all(),
    }
    return render(request, 'main/index.html', context=context)

        receipts = Receipt.objects.filter(owner=request.user).order_by('-date', '-id').prefetch_related('products')[:100]

        for receipt in receipts:
            receipt.formset = ProductFormSet(queryset=receipt.products.all())

        context['receipts'] = receipts

    return render(request, 'main/index.html', context=context)


@login_required
def delete_receipt(request, receipt_id):
    if request.method == 'POST':
        receipt = get_object_or_404(Receipt, id=receipt_id)
        receipt.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)