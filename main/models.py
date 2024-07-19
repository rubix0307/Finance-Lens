from django.db import models
from django.utils.translation import gettext_lazy
# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    price = models.DecimalField(max_digits=20, decimal_places=5, verbose_name=gettext_lazy('Price'))
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=gettext_lazy('Category'))