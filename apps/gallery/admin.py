from django.contrib import admin
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'is_archived', 'created_at')
    list_filter = ('category', 'is_archived')
    search_fields = ('title', 'caption')
