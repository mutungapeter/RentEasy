# mixins.py
from django.db import models

class TenantMixin(models.Model):
    is_tenant = models.BooleanField(default=False)

    class Meta:
        abstract = True

class LandLordMixin(models.Model):
    is_landlord = models.BooleanField(default=False)

    class Meta:
        abstract = True
