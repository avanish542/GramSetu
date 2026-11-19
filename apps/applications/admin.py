from django.contrib import admin
from .models import ServiceApplication, ApplicationDocument

class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    readonly_fields = ('file_size', 'mime_type')

@admin.register(ServiceApplication)
class ServiceApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'applicant_name', 'service', 'status', 'applicant_phone', 'created_at')
    list_filter = ('status', 'service', 'village')
    search_fields = ('application_number', 'applicant_name', 'applicant_phone', 'applicant__username')
    inlines = [ApplicationDocumentInline]
