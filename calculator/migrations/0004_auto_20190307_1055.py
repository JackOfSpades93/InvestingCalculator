# Generated by Django 2.1.7 on 2019-03-07 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_auto_20190305_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='ticker',
            field=models.CharField(max_length=100),
        ),
    ]
