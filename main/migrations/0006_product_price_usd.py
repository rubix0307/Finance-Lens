# Generated by Django 5.0.6 on 2024-07-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_currencyratehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]