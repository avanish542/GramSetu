from django.db import models
from apps.core.models import TimeStampedModel

class Village(TimeStampedModel):
    name = models.CharField(max_length=100)
    gram_panchayat = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    population = models.PositiveIntegerField(default=0)
    households = models.PositiveIntegerField(default=0)
    total_wards = models.PositiveIntegerField(default=0)
    history = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='village/hero/', blank=True, null=True)

    class Meta:
        verbose_name = "Village"
        verbose_name_plural = "Villages"

    def __str__(self):
        return f"{self.name}, {self.district} ({self.state})"


class Ward(TimeStampedModel):
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='wards')
    ward_number = models.PositiveIntegerField()
    ward_name = models.CharField(max_length=100)
    representative_name = models.CharField(max_length=100, blank=True)
    representative_phone = models.CharField(max_length=15, blank=True)
    population = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('village', 'ward_number')
        ordering = ['ward_number']

    def __str__(self):
        return f"Ward {self.ward_number} - {self.ward_name}"


class VillageInfo(TimeStampedModel):
    village = models.OneToOneField(Village, on_delete=models.CASCADE, related_name='info')
    schools_count = models.PositiveIntegerField(default=0)
    health_centers_count = models.PositiveIntegerField(default=0)
    water_facilities_overview = models.TextField(blank=True)
    electricity_coverage_percent = models.DecimalField(max_length=5, max_digits=5, decimal_places=2, default=100.00)
    waste_management_overview = models.TextField(blank=True)
    panchayat_office_address = models.TextField(blank=True)
    panchayat_contact_email = models.EmailField(blank=True)
    panchayat_contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Information & Statistics - {self.village.name}"


class RelatedPanchayat(TimeStampedModel):
    RELATION_CHOICES = (
        ('PRIMARY_GP', 'Tenuhari Gram Panchayat'),
        ('REVENUE_VILLAGE', 'Villages under Tenuhari Gram Panchayat'),
        ('SAHJANWA_GP', 'Other Sahjanwa-area Gram Panchayats'),
        ('NEARBY_VILLAGE', 'Nearby villages where verified geographic information is available'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=RELATION_CHOICES, default='SAHJANWA_GP')
    tehsil = models.CharField(max_length=100, default='Sahjanwa')
    district = models.CharField(max_length=100, default='Gorakhpur')
    state = models.CharField(max_length=100, default='Uttar Pradesh')
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class VillageCondition(TimeStampedModel):
    STATUS_CHOICES = (
        ('GOOD', 'Good / Satisfactory'),
        ('MODERATE', 'Moderate / Acceptable'),
        ('NEEDS_ATTENTION', 'Needs Attention'),
        ('CRITICAL', 'Critical / Urgent Repair'),
        ('UNKNOWN', 'Unknown / Unverified'),
    )

    CATEGORY_CHOICES = (
        ('Roads', 'Roads'),
        ('Drainage', 'Drainage'),
        ('Drinking Water', 'Drinking Water'),
        ('Electricity', 'Electricity'),
        ('Street Lighting', 'Street Lighting'),
        ('Schools', 'Schools'),
        ('Health Facilities', 'Health Facilities'),
        ('Sanitation', 'Sanitation'),
        ('Waste Management', 'Waste Management'),
        ('Internet/Digital Connectivity', 'Internet/Digital Connectivity'),
        ('Agriculture', 'Agriculture'),
        ('Transportation', 'Transportation'),
        ('Public Buildings', 'Public Buildings'),
        ('Water Bodies', 'Water Bodies'),
    )

    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='conditions', null=True, blank=True)
    related_panchayat = models.ForeignKey(RelatedPanchayat, on_delete=models.CASCADE, related_name='conditions', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MODERATE')
    description = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    source = models.CharField(max_length=150, default='Demo Data / Sample Assessment')
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['category']

    def __str__(self):
        loc_name = self.village.name if self.village else (self.related_panchayat.name if self.related_panchayat else "Location")
        return f"{loc_name} - {self.category}: {self.get_condition_status_display()}"
