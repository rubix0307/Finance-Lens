from django.contrib import admin

from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_currency_code', 'price', 'price_usd')

    def get_currency_code(self, obj):
        return obj.receipt.currency.code

    get_currency_code.short_description = 'Currency Code'

admin.site.register(Product, ProductAdmin)