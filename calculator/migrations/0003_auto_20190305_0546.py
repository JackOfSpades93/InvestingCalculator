# Generated by Django 2.1.7 on 2019-03-05 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0002_auto_20190305_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetdatevalue',
            name='adjusted_close',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='close',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='dividend',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='high',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='low',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='open',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='assetdatevalue',
            name='volume',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
