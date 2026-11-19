from django.contrib import admin
from .models import GovernmentScheme

@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'department', 'deadline', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'department', 'benefits')
    prepopulated_fields = {'slug': ('name',)}
