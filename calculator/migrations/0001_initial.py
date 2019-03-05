# Generated by Django 2.1.7 on 2019-03-04 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('last_update', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetDateValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('low', models.FloatField()),
                ('high', models.FloatField()),
                ('adjusted_close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('dividend', models.FloatField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calculator.Asset')),
            ],
        ),
    ]
