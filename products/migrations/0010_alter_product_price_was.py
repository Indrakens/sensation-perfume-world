# Generated by Django 3.2.23 on 2024-01-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_include'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_was',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]