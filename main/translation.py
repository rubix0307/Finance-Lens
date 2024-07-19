from modeltranslation.translator import register, TranslationOptions
from .models import Product, ProductCategory

@register(ProductCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)