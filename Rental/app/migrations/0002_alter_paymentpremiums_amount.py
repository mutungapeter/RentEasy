# Generated by Django 4.2.6 on 2023-10-17 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentpremiums',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
