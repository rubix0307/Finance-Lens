# Generated by Django 5.0.6 on 2024-07-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_product_name_en_product_name_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_ua',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='name_ua',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
    ]
