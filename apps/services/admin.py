from django.contrib import admin
from .models import PanchayatService, ServiceRequirement

class ServiceRequirementInline(admin.TabularInline):
    model = ServiceRequirement
    extra = 1

@admin.register(PanchayatService)
class PanchayatServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'processing_days', 'fee', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceRequirementInline]
