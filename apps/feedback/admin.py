from django.contrib import admin
from .models import ProjectFeedback

@admin.register(ProjectFeedback)
class ProjectFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'project__name', 'comment')
