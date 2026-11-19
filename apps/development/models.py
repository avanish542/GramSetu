from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.core.models import TimeStampedModel

class ProjectCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='hammer', help_text="Tailwind or SVG icon name")

    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectStatus(models.TextChoices):
    PLANNED = 'PLANNED', 'Planned'
    APPROVED = 'APPROVED', 'Approved'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    ON_HOLD = 'ON_HOLD', 'On Hold'
    CANCELLED = 'CANCELLED', 'Cancelled'


class DevelopmentProject(TimeStampedModel):
    project_id = models.CharField(max_length=30, unique=True, help_text="Unique Identifier e.g. PRJ-2026-0001")
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProjectCategory, on_delete=models.PROTECT, related_name='projects')
    description = models.TextField()
    location = models.CharField(max_length=200)
    village = models.ForeignKey('village.Village', on_delete=models.CASCADE, related_name='projects')
    ward = models.ForeignKey('village.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    approved_budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    funding_source = models.CharField(max_length=150, help_text="e.g. 15th Finance Commission, MGNREGA, State Govt")
    
    start_date = models.DateField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    
    contractor = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNED)
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Progress from 0 to 100%"
    )
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['ward']),
            models.Index(fields=['start_date']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.project_id} - {self.name}"

    @property
    def remaining_budget(self):
        return max(0, self.approved_budget - self.amount_spent)


class ProjectImageStage(models.TextChoices):
    BEFORE = 'BEFORE', 'Before Work'
    DURING = 'DURING', 'Work In Progress'
    AFTER = 'AFTER', 'After Completion'


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(DevelopmentProject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')
    stage_type = models.CharField(max_length=20, choices=ProjectImageStage.choices, default=ProjectImageStage.DURING)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.get_stage_type_display()}"


class ProjectExpense(TimeStampedModel):
    project = models.ForeignKey(DevelopmentProject, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    spent_date = models.DateField()
    invoice_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} (₹{self.amount}) - {self.project.name}"


class ProjectTimeline(TimeStampedModel):
    project = models.ForeignKey(DevelopmentProject, on_delete=models.CASCADE, related_name='timeline_events')
    title = models.CharField(max_length=150)
    event_date = models.DateField()
    status_reached = models.CharField(max_length=20, choices=ProjectStatus.choices, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} on {self.event_date}"
