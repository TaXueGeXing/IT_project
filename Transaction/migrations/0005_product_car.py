# Generated by Django 5.0.1 on 2024-03-05 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0004_alter_order_buyerid'),
        ('car_wiki', '0002_car_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='car_wiki.car'),
        ),
    ]