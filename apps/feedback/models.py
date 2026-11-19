from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.development.models import DevelopmentProject

class ProjectFeedback(TimeStampedModel):
    project = models.ForeignKey(DevelopmentProject, on_delete=models.CASCADE, related_name='feedback_entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_feedback')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (Poor) to 5 (Excellent)"
    )
    comment = models.TextField()
    photo = models.ImageField(upload_to='feedback/', blank=True, null=True)

    class Meta:
        unique_together = ('project', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rating {self.rating}/5 on {self.project.name}"
