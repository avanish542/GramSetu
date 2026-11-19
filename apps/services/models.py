from django.db import models
from apps.core.models import TimeStampedModel

class PanchayatService(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, default='Certificates & Documents')
    description = models.TextField()
    eligibility = models.TextField()
    required_documents = models.TextField(help_text="Bullet points of required document names")
    processing_days = models.PositiveIntegerField(default=7, help_text="Estimated processing time in days")
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, default='document-text')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceRequirement(TimeStampedModel):
    service = models.ForeignKey(PanchayatService, on_delete=models.CASCADE, related_name='requirements')
    document_name = models.CharField(max_length=150)
    is_mandatory = models.BooleanField(default=True)
    instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.document_name} ({'Mandatory' if self.is_mandatory else 'Optional'}) - {self.service.name}"
