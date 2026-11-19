from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class NoticeCategory(models.TextChoices):
    GRAM_SABHA = 'Gram Sabha', 'Gram Sabha'
    WATER_SUPPLY = 'Water Supply', 'Water Supply'
    ROAD_WORK = 'Road Work', 'Road Work'
    HEALTH_CAMP = 'Health Camp', 'Health Camp'
    SCHEME = 'Government Scheme', 'Government Scheme'
    EDUCATION = 'Education', 'Education'
    EMERGENCY = 'Emergency', 'Emergency'
    GENERAL = 'General', 'General'


class Notice(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=NoticeCategory.choices, default=NoticeCategory.GENERAL)
    description = models.TextField()
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of homepage / notice board")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_pinned', '-published_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
