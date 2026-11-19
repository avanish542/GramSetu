from django.db import models
from apps.core.models import TimeStampedModel

class GalleryCategory(models.TextChoices):
    DEVELOPMENT = 'Development Work', 'Development Work'
    EVENTS = 'Village Events', 'Village Events'
    GRAM_SABHA = 'Gram Sabha', 'Gram Sabha'
    CLEANLINESS = 'Cleanliness Drive', 'Cleanliness Drive'
    PLANTATION = 'Plantation', 'Plantation'
    SPORTS = 'Sports', 'Sports'
    EDUCATION = 'Education', 'Education'
    CULTURAL = 'Cultural Events', 'Cultural Events'


class GalleryItem(TimeStampedModel):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=GalleryCategory.choices, default=GalleryCategory.EVENTS)
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True)
    event_date = models.DateField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
