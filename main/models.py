from django.contrib.auth import get_user_model
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)


class CurrencyRateHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    per_usd = models.DecimalField(max_digits=14, decimal_places=7)
    date = models.DateField()

    class Meta:
        unique_together = ('currency', 'per_usd', 'date')

class Receipt(models.Model):
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    shop_address = models.CharField(max_length=1024, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    photo = models.ImageField(upload_to='bot/', null=True, blank=True, max_length=1024)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # TODO Add ForeignKey to family group

    def __str__(self):
        return self.shop_name

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_original = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        if not self.pk and not self.name_original:
            self.name_original = self.name

        super(Product, self).save(*args, **kwargs)
        return self

    class Meta:
        ordering = ['id']