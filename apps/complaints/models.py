from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class ComplaintCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='exclamation-circle')

    class Meta:
        verbose_name_plural = "Complaint Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ComplaintPriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'


class ComplaintStatus(models.TextChoices):
    SUBMITTED = 'SUBMITTED', 'Submitted'
    ACKNOWLEDGED = 'ACKNOWLEDGED', 'Acknowledged'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'


class Complaint(TimeStampedModel):
    ticket_number = models.CharField(max_length=30, unique=True, help_text="Format e.g. CMP-2026-0001")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    category = models.ForeignKey(ComplaintCategory, on_delete=models.PROTECT, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    village = models.ForeignKey('village.Village', on_delete=models.CASCADE, related_name='complaints')
    ward = models.ForeignKey('village.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    
    priority = models.CharField(max_length=20, choices=ComplaintPriority.choices, default=ComplaintPriority.MEDIUM)
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.SUBMITTED)
    
    photo = models.ImageField(upload_to='complaints/', blank=True, null=True)
    video = models.FileField(upload_to='complaints/videos/', blank=True, null=True)
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )
    
    internal_notes = models.TextField(blank=True, help_text="Strictly private admin notes, hidden from villagers")
    resolution_photo = models.ImageField(upload_to='complaints/resolutions/', blank=True, null=True)
    resolution_comment = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['ward']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"


class ComplaintUpdate(TimeStampedModel):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices)
    note = models.TextField()
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="If True, villager can see this update step")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Update for {self.complaint.ticket_number} ({self.get_status_display()})"
