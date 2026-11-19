from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'model_name', 'object_id', 'ip_address')
    list_filter = ('model_name', 'action')
    search_fields = ('actor__username', 'description', 'model_name', 'object_id')
    readonly_fields = ('actor', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
