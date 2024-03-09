# Generated by Django 5.0.1 on 2024-03-09 16:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Transaction', '0001_initial'),
        ('car_wiki', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ProductID', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Description', models.TextField()),
                ('Title', models.CharField(max_length=100)),
                ('Location', models.TextField()),
                ('SellerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='car_wiki.car')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('OrderID', models.AutoField(primary_key=True, serialize=False)),
                ('Time', models.DateTimeField()),
                ('IsBanned', models.BooleanField()),
                ('IsFinished', models.BooleanField()),
                ('IsAgreed', models.BooleanField()),
                ('BuyerID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_orders', to=settings.AUTH_USER_MODEL)),
                ('SellerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_orders', to=settings.AUTH_USER_MODEL)),
                ('ProductID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Transaction.product')),
            ],
        ),
    ]
