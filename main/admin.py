from django.contrib import admin

from .models import Product, CurrencyRateHistory, ProductCategory, Receipt


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_currency_code', 'price', 'get_category')
    list_filter = ('category',)

    def get_currency_code(self, obj):
        return obj.receipt.currency.code

    get_currency_code.short_description = 'Currency Code'

    def get_category(self, obj):
        return f'{obj.category.name} {obj.category.id}'

    get_category.short_description = 'Category'


class CurrencyRateHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'per_usd', 'date',)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'shop_address', 'currency', 'date', 'photo', 'owner', )


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(CurrencyRateHistory, CurrencyRateHistoryAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
