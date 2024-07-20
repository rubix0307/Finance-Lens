from django import template
from modeltranslation.utils import get_language

register = template.Library()

@register.filter(name='get_translated_field')
def get_translated_field(instance, field_name):
    current_language = get_language()
    translated_field_name = f"{field_name}_{current_language}"
    return getattr(instance, translated_field_name, getattr(instance, field_name))
