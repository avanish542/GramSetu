from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_by', 'published_at', 'is_pinned', 'is_published', 'expiry_date')
    list_filter = ('category', 'is_pinned', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
