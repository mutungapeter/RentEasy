# Generated by Django 4.2.6 on 2023-10-17 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_payment_payment_premium'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentLog',
        ),
    ]
