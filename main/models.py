from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from scraper.currency.scraper import CurrencyScraper


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.code


class CurrencyRateHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    per_usd = models.DecimalField(max_digits=14, decimal_places=7)
    date = models.DateField()

    def __str__(self):
        return f'{self.id}: {self.per_usd}'

    class Meta:
        get_latest_by = ['date']


class Section(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    users = models.ManyToManyField(get_user_model(), through='SectionUser', related_name='sections', blank=True)

    def get_user_currency(self, user):
        return SectionUser.objects.get(section=self, user=user).currency

    def set_user_currency(self, user, currency) -> bool:
        try:
            section_user = SectionUser.objects.get(section=self, user=user)
            section_user.currency = currency
            section_user.save()
        except SectionUser.DoesNotExists:
            return False
        return True


class SectionUser(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    is_base = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def set_base_section_for_user(user, section, **kwargs):
        SectionUser.objects.filter(user=user, is_base=True).update(is_base=False)

        section_user, _ = SectionUser.objects.update_or_create(
            user=user,
            section=section,
            defaults={'is_base': True} | kwargs
        )


        return section_user



class Receipt(models.Model):
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    shop_address = models.CharField(max_length=1024, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    photo = models.ImageField(upload_to='bot/', null=True, blank=True, max_length=1024)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)

    def update_price(self):
        products = Product.objects.filter(receipt=self)
        for product in products:
            product.update_or_create_product_price_base_rate()

    def __str__(self):
        return f'{self.shop_name}'

    class Meta:
        indexes = [
            models.Index(fields=['date'], name='idx_date'),
            models.Index(fields=['owner'], name='idx_owner'),
            models.Index(fields=['owner', 'date'], name='idx_owner_date')
        ]


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
        is_new = None

        if not self.pk:
            is_new = True

        if not self.name_original:
            self.name_original = self.name

        super(Product, self).save(*args, **kwargs)

        if is_new:
            self.update_or_create_product_price_base_rate()

        return self

    def update_or_create_product_price_base_rate(self):
        currency = self.receipt.section.currency
        price, currency = self.get_price_in_currency(currency=currency)

        product_price, is_created = ProductPrice.objects.update_or_create(
            product=self,
            currency=currency,
            defaults={'price': price},
        )
        return product_price

    def get_price_in_currency(self, currency: Currency, use_date_filter: bool = True):
        try:

            if use_date_filter:
                date_filter = {'date': self.receipt.date}
            else:
                date_filter = {}

            rate_to_usd: CurrencyRateHistory = (
                CurrencyRateHistory.objects
                .filter(
                    currency=self.receipt.currency,
                    **date_filter
                ).latest()
            )
            rate_to_currency: CurrencyRateHistory = (
                CurrencyRateHistory.objects
                .filter(
                    currency=currency,
                    date=rate_to_usd.date,
                ).latest()
            )

            price_in_usd = Decimal(self.price) / Decimal(rate_to_usd.per_usd)
            price_in_currency = price_in_usd * rate_to_currency.per_usd

            return price_in_currency, currency
        except CurrencyRateHistory.DoesNotExist:
            scraper = CurrencyScraper(currency_symbol='USD', date=self.receipt.date)
            rate_history = scraper.write_rate_history()

            use_date_filter = False
            if rate_history:
                use_date_filter = True
            return self.get_price_in_currency(currency=currency, use_date_filter=use_date_filter)


    class Meta:
        ordering = ['id']


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('product', 'currency')
