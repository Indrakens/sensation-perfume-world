# Generated by Django 3.2.23 on 2024-01-02 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20240102_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='include',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
