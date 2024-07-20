from django.db import models
from django.utils.translation import gettext_lazy

from utils import PauseLanguage


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=gettext_lazy('Price'))
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=gettext_lazy('Category'))

    def __init__(self, *args, **kwargs):
        if args:
            self.original_name = args[self.get_field_number(self._meta.get_field('name'))]
        super(Product, self).__init__(*args, **kwargs)

    def get_field_number(self, search_field: str):
        for num, field in enumerate(self._meta.get_fields()):
            if field == search_field:
                return num

    def save(self, *args, **kwargs):
        with PauseLanguage():
            self.name = self.original_name
            super(Product, self).save(*args, **kwargs)

        return self



    class Meta:
        ordering = ['id']