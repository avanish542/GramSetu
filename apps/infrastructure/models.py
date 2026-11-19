from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class InfraCategory(models.TextChoices):
    PANCHAYAT_BHAWAN = 'PANCHAYAT_BHAWAN', 'Panchayat Bhawan'
    SCHOOL = 'SCHOOL', 'School'
    HEALTH_CENTRE = 'HEALTH_CENTRE', 'Health Centre'
    ROAD_PROJECT = 'ROAD_PROJECT', 'Road Project'
    WATER_TANK = 'WATER_TANK', 'Water Tank / Supply'
    HAND_PUMP = 'HAND_PUMP', 'Hand Pump'
    STREET_LIGHT = 'STREET_LIGHT', 'Street Light'
    PUBLIC_TOILET = 'PUBLIC_TOILET', 'Public Toilet'
    PARK = 'PARK', 'Park / Playground'
    WASTE_COLLECTION = 'WASTE_COLLECTION', 'Waste Collection Point'


class InfraStatus(models.TextChoices):
    OPERATIONAL = 'OPERATIONAL', 'Operational'
    UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'Under Maintenance'
    PROPOSED = 'PROPOSED', 'Proposed / In Construction'
    OUT_OF_ORDER = 'OUT_OF_ORDER', 'Out of Order'


class InfrastructureItem(TimeStampedModel):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=40, choices=InfraCategory.choices)
    description = models.TextField(blank=True)
    village = models.ForeignKey('village.Village', on_delete=models.CASCADE, related_name='infrastructure')
    ward = models.ForeignKey('village.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='infrastructure')
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    status = models.CharField(max_length=30, choices=InfraStatus.choices, default=InfraStatus.OPERATIONAL)
    image = models.ImageField(upload_to='infrastructure/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Infrastructure Item"
        verbose_name_plural = "Infrastructure Items"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
