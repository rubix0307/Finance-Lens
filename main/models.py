from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)