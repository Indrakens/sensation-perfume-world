# Generated by Django 3.2.23 on 2023-12-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_include'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_was',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
