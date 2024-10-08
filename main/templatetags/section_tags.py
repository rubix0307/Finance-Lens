from django import template
from django.utils import timezone
from django.db.models.functions import TruncMonth
from main.models import Receipt


register = template.Library()


@register.simple_tag
def get_available_months(section_id):
    dates = (Receipt.objects
             .filter(section__id=section_id)
             .annotate(month=TruncMonth('date', tzinfo=timezone.get_default_timezone()))
             .values_list('month', flat=True)
             .distinct()
             .order_by('month')
             )
    return list(dates)
