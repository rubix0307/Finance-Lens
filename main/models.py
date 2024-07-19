from django.db import models
from django.utils.translation import gettext_lazy
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    price = models.DecimalField(max_digits=20, decimal_places=5, verbose_name=gettext_lazy('Price'))
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=gettext_lazy('Category'))

    def __init__(self, *args, **kwargs):
        self.original_name = args[self.get_field_number(self._meta.get_field('name'))]
        super(Product, self).__init__(*args, **kwargs)

    def get_field_number(self, search_field: str):
        for num, field in enumerate(self._meta.get_fields()):
            if field == search_field:
                return num
