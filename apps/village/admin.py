from django.contrib import admin
from .models import Village, Ward, VillageInfo, VillageCondition, RelatedPanchayat

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'gram_panchayat', 'block', 'district', 'state', 'population', 'households', 'total_wards')
    search_fields = ('name', 'gram_panchayat', 'district')
    list_filter = ('state', 'district')

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_number', 'ward_name', 'village', 'representative_name', 'representative_phone')
    list_filter = ('village',)
    search_fields = ('ward_name', 'representative_name')

@admin.register(VillageInfo)
class VillageInfoAdmin(admin.ModelAdmin):
    list_display = ('village', 'schools_count', 'health_centers_count', 'electricity_coverage_percent')

@admin.register(VillageCondition)
class VillageConditionAdmin(admin.ModelAdmin):
    list_display = ('category', 'condition_status', 'village', 'related_panchayat', 'source', 'verified', 'updated_at')
    list_filter = ('condition_status', 'verified', 'category')
    search_fields = ('category', 'description', 'remarks')

@admin.register(RelatedPanchayat)
class RelatedPanchayatAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'tehsil', 'district', 'state', 'distance_km')
    list_filter = ('category', 'tehsil', 'district')
    search_fields = ('name', 'notes')

