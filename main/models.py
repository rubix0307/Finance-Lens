from django.db import models
from django.utils.translation import gettext_lazy



class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    name_original = models.CharField(max_length=255, verbose_name=gettext_lazy('Original'))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=gettext_lazy('Price'))
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=gettext_lazy('Category'))

    def save(self, *args, **kwargs):
        if not self.pk and self.name_original:
            self.name_original = self.name

        super(Product, self).save(*args, **kwargs)
        return self

    class Meta:
        ordering = ['id']