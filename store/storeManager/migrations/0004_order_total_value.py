# Generated by Django 4.2.14 on 2025-01-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeManager', '0003_orderitem_stock_state_alter_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_value',
            field=models.IntegerField(default=0),
        ),
    ]