from django.contrib import admin
from .models import InfrastructureItem

@admin.register(InfrastructureItem)
class InfrastructureItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ward', 'status', 'latitude', 'longitude')
    list_filter = ('category', 'status', 'ward', 'village')
    search_fields = ('name', 'description')
