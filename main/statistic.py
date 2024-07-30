from collections import defaultdict

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from main.models import ProductCategory, Receipt


def get_user_statistic():
    receipts = Receipt.objects.filter(date__isnull=False).annotate(
        month=TruncMonth('date')
    ).prefetch_related('products__category', 'currency').values(
        'month',
        'products__category',
        'products__price_usd',
        'currency__code'
    ).annotate(
        total_usd=Sum('products__price_usd'),
        currency_sum=Sum('products__price')
    )

    result = defaultdict(
        lambda: defaultdict(lambda: {'category': None, 'total_usd': 0, 'currencies': defaultdict(int)}))

    categories_cache = {}

    for item in receipts:
        month = item['month'].strftime('%Y-%m')
        category_id = item['products__category']
        currency = item['currency__code']
        total_usd = item['total_usd'] or 0
        currency_sum = item['currency_sum'] or 0

        if category_id not in categories_cache:
            categories_cache[category_id] = ProductCategory.objects.get(id=category_id)

        category_obj = categories_cache[category_id]

        result[month][category_id]['category'] = category_obj
        result[month][category_id]['total_usd'] += total_usd
        result[month][category_id]['currencies'][currency] += currency_sum

    answer = []
    for month, categories in result.items():
        d = {'month': month}
        d['categories'] = {
            data['category'].name: {
                'total_usd': data['total_usd'],
                'currencies': data['currencies']
            } for category_id, data in categories.items()
        }
        answer.append(d)

    return answer