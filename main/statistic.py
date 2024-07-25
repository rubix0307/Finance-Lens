import datetime
from collections import defaultdict
from dataclasses import dataclass

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from main.models import ProductCategory, Receipt



@dataclass
class Value:
    name: str
    value: str|float

@dataclass
class Statistic:
    date: str
    categories: list[Value]
    total: list[Value]

def get_monthly_expenses(user) -> list[Statistic]:
    # Группировка данных по месяцам с использованием TruncMonth
    receipts = Receipt.objects.filter(owner=user).annotate(month=TruncMonth('date'))

    # Структура для хранения результатов
    monthly_expenses = defaultdict(lambda: {'total_by_currency': defaultdict(float),
                                            'categories_by_currency': defaultdict(lambda: defaultdict(float))})

    for receipt in receipts:
        month = receipt.month.strftime("%Y-%m")
        currency_code = receipt.currency.code

        # Суммарное потраченное количество денег (группируя по currency)
        total_spent = receipt.products.aggregate(total=Sum('price'))['total'] or 0
        monthly_expenses[month]['total_by_currency'][currency_code] += float(total_spent)

        # Потраченное количество денег по категориям (группируя по currency)
        category_spent = receipt.products.values('category').annotate(total=Sum('price'))

        for category in category_spent:
            category_obj = ProductCategory.objects.get(pk=category['category'])
            spent = category['total'] or 0
            monthly_expenses[month]['categories_by_currency'][category_obj][currency_code] += float(spent)

    statistics = []

    for month, data in monthly_expenses.items():
        total = [Value(name=currency, value=total_spent) for currency, total_spent in
                 data['total_by_currency'].items()]

        categories = []
        for category, currencies in data['categories_by_currency'].items():
            category_values = [Value(name=currency, value=spent) for currency, spent in currencies.items()]
            categories.append(Value(name=category, value=category_values))

        statistics.append(Statistic(date=month, categories=categories, total=total))

    return statistics

