from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class NotificationType(models.TextChoices):
    APPLICATION = 'APPLICATION', 'Application Status'
    COMPLAINT = 'COMPLAINT', 'Complaint Update'
    NOTICE = 'NOTICE', 'New Notice'
    PROJECT = 'PROJECT', 'Development Project Update'
    SYSTEM = 'SYSTEM', 'System Notification'


class InAppNotification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
