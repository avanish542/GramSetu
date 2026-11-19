from django.contrib import admin
from .models import ComplaintCategory, Complaint, ComplaintUpdate

class ComplaintUpdateInline(admin.TabularInline):
    model = ComplaintUpdate
    extra = 1

@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'title', 'user', 'category', 'priority', 'status', 'ward', 'created_at')
    list_filter = ('status', 'priority', 'category', 'ward')
    search_fields = ('ticket_number', 'title', 'user__username', 'user__first_name', 'location')
    inlines = [ComplaintUpdateInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'status', 'updated_by', 'is_public', 'created_at')
