from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.core.cache import cache
from scraper.currency.scraper import CurrencyScraper

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)


class CurrencyRateHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    per_usd = models.DecimalField(max_digits=14, decimal_places=7)
    date = models.DateField()

    class Meta:
        unique_together = ('currency', 'per_usd', 'date')
        get_latest_by = ['date']

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
    price_usd = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        if not self.pk and not self.name_original:
            self.name_original = self.name

        self.price_usd = Decimal(self.price or 0) / (self.get_usd_conversion_rate() or Decimal(1))

        super(Product, self).save(*args, **kwargs)
        return self

    def get_usd_conversion_rate(self):
        cache_key = f'{self.get_usd_conversion_rate.__name__}_{self.receipt.currency.code}_{self.receipt.date.strftime("%Y-%m-%d")}'

        cached_rate = cache.get(cache_key)
        if cached_rate is not None:
            return cached_rate

        rate = None
        try:
            rate = CurrencyRateHistory.objects.filter(currency=self.receipt.currency, date=self.receipt.date).latest()
        except CurrencyRateHistory.DoesNotExist:
            pass

        if not rate or ((rate.date.year, rate.date.month, rate.date.day) != (self.receipt.date.year, self.receipt.date.month, self.receipt.date.day)):
            scraper = CurrencyScraper(currency_symbol='USD', date=self.receipt.date)
            scraper.write_rate_history()

            rate = CurrencyRateHistory.objects.filter(currency=self.receipt.currency).latest()

        cache.set(cache_key, rate.per_usd, timeout=20) # TODO update timeout
        return rate.per_usd


    class Meta:
        ordering = ['id']