from django.db import models
from apps.core.models import TimeStampedModel

class SchemeCategory(models.TextChoices):
    HOUSING = 'Housing', 'Housing'
    PENSION = 'Pension', 'Pension'
    EDUCATION = 'Education', 'Education'
    AGRICULTURE = 'Agriculture', 'Agriculture'
    EMPLOYMENT = 'Employment', 'Employment'
    HEALTH = 'Health', 'Health'
    WOMEN_CHILD = 'Women & Child Welfare', 'Women & Child Welfare'
    FINANCIAL = 'Financial Assistance', 'Financial Assistance'
    OTHER = 'Other', 'Other'

class GovernmentScheme(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=SchemeCategory.choices, default=SchemeCategory.OTHER)
    department = models.CharField(max_length=150, help_text="e.g. Ministry of Rural Development, Dept of Social Welfare")
    description = models.TextField()
    eligibility = models.TextField()
    benefits = models.TextField()
    required_documents = models.TextField()
    application_process = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    official_link = models.URLField(max_length=500, blank=True, help_text="Official government URL")
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, default='academic-cap')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
