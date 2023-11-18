# Generated by Django 4.2.3 on 2023-11-18 13:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_departments_margin_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('sale_date', models.DateTimeField(default=datetime.datetime(2023, 11, 18, 13, 45, 33, 932495))),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED')], default='ACCEPTED', max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_order_product', to='products.products')),
            ],
            options={
                'verbose_name': 'Sale Order',
                'verbose_name_plural': 'Sale Orders',
                'db_table': 'sale_order',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('unit_cost', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('purchase_date', models.DateTimeField(default=datetime.datetime(2023, 11, 18, 13, 45, 33, 932013))),
                ('status', models.CharField(choices=[('RECEIVED', 'RECEIVED'), ('CANCELLED', 'CANCELLED')], default='RECEIVED', max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_product', to='products.products')),
            ],
            options={
                'verbose_name': 'Purchase Order',
                'verbose_name_plural': 'Purchase Orders',
                'db_table': 'purchase_order',
                'ordering': ['-created_at'],
            },
        ),
    ]