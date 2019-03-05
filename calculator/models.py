from django.db import models
from django.contrib import admin


# Create your models here.

class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    last_update = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.ticker + " | " + self.name


admin.site.register(Asset)


class AssetDateValue(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    date = models.DateField()
    open = models.FloatField(default=None, blank=True, null=True)
    close = models.FloatField(default=None, blank=True, null=True)
    low = models.FloatField(default=None, blank=True, null=True)
    high = models.FloatField(default=None, blank=True, null=True)
    adjusted_close = models.FloatField(default=None, blank=True, null=True)
    volume = models.BigIntegerField(default=None, blank=True, null=True)
    dividend = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.asset.ticker + " | " + str(self.date)


admin.site.register(AssetDateValue)
