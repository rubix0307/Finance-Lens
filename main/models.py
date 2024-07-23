from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy



class Currency(models.Model):
    code = models.CharField(max_length=3)

class Receipt(models.Model):
    shop_name = models.CharField(max_length=255)
    shop_address = models.CharField(max_length=1024)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.IntegerField()
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