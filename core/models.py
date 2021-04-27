# Create your models here.
from __future__ import unicode_literals

# from country_regions.models import Region, Country
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AuditTrail(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_trail_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_trail_updated')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skills(AuditTrail):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class MainSector(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class SubSector(models.Model):
    main_sector = models.ForeignKey(MainSector, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']
        unique_together = [('main_sector', 'name')]

    def __str__(self):
        return f'{self.main_sector} : {self.name}'


class AbstractAddress(models.Model):
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text="Country")
    # state = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, help_text="Region/State")
    country = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Country"
    )
    state = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Region/State"
    )
    district = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="District"
    )
    town_city = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Village/Taluka/Town/City."
    )
    street_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Street name"
    )
    address_line = models.CharField(
        max_length=255,
        blank=True,
        help_text="House name/number"
    )
    post_code = models.CharField(
        max_length=15,
        blank=True,
        default='',
        help_text="Post/ZIP code"
    )
    plus_code = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="Plus code (https://maps.google.com/pluscodes/)"
    )

    class Meta:
        abstract = True
