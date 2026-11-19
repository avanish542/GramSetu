from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.services.models import PanchayatService

class ApplicationStatus(models.TextChoices):
    SUBMITTED = 'SUBMITTED', 'Submitted'
    UNDER_VERIFICATION = 'UNDER_VERIFICATION', 'Under Verification'
    ADDITIONAL_INFO_REQUIRED = 'ADDITIONAL_INFO_REQUIRED', 'Additional Information Required'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class ServiceApplication(TimeStampedModel):
    application_number = models.CharField(max_length=30, unique=True, help_text="Format e.g. APP-2026-0001")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_applications')
    service = models.ForeignKey(PanchayatService, on_delete=models.PROTECT, related_name='applications')
    village = models.ForeignKey('village.Village', on_delete=models.CASCADE, related_name='applications')
    ward = models.ForeignKey('village.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    
    applicant_name = models.CharField(max_length=150)
    applicant_phone = models.CharField(max_length=15)
    applicant_address = models.TextField()
    
    status = models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED)
    remarks = models.TextField(blank=True, help_text="Public status remarks for applicant")
    rejection_reason = models.TextField(blank=True, help_text="Mandatory if status is REJECTED")
    
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_applications'
    )
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['application_number']),
            models.Index(fields=['status']),
            models.Index(fields=['applicant']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.application_number} - {self.service.name} by {self.applicant_name}"


class ApplicationDocument(TimeStampedModel):
    application = models.ForeignKey(ServiceApplication, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=150)
    file = models.FileField(upload_to='private_documents/applications/%Y/%m/')
    mime_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0, help_text="File size in bytes")

    def __str__(self):
        return f"{self.document_name} for {self.application.application_number}"
