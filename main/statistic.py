import time
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth

from main.models import ProductCategory, Receipt


def get_section_statistic(section):
    receipts = Receipt.objects.filter(section=section, date__isnull=False).annotate(
        base_currency=F('section__currency__code'),
        base_currency_price=Sum(
            F('products__prices__price'),
            filter=Q(products__prices__currency=F('section__currency'))
        ),
        month=TruncMonth('date'),
    ).prefetch_related('products__category', 'currency').values(
        'base_currency_price',
        'base_currency',
        'month',
        'currency__code',
        'products__category',
    ).annotate(
        currency_sum=Sum('products__price')
    )

    result = defaultdict(
        lambda: defaultdict(lambda: {'category': None, 'base_currency': None, 'total_base_currency': 0, 'currencies': defaultdict(int)}))

    categories_cache = {}

    for item in receipts:
        month = item['month'].strftime('%Y-%m')
        category_id = item['products__category']
        currency = item['currency__code']
        currency_sum = item['currency_sum'] or 0

        if category_id and (category_id not in categories_cache):
            categories_cache[category_id] = ProductCategory.objects.get(id=category_id)

        if category_id:
            category_obj = categories_cache[category_id]

            result[month][category_id]['category'] = category_obj
            result[month][category_id]['base_currency'] = item['base_currency']
            result[month][category_id]['total_base_currency'] += item['base_currency_price']
            result[month][category_id]['currencies'][currency] += currency_sum

    answer = []
    for month, categories in result.items():
        d = {'month': month}
        d['categories'] = {
            data['category'].name: {
                'base_currency': data['base_currency'],
                'total_base_currency': data['total_base_currency'],
                'currencies': data['currencies']
            } for category_id, data in categories.items()
        }
        answer.append(d)

    return answer