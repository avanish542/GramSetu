from django.contrib import admin
from .models import ProjectCategory, DevelopmentProject, ProjectImage, ProjectExpense, ProjectTimeline

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectExpenseInline(admin.TabularInline):
    model = ProjectExpense
    extra = 1

class ProjectTimelineInline(admin.TabularInline):
    model = ProjectTimeline
    extra = 1

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(DevelopmentProject)
class DevelopmentProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name', 'category', 'status', 'progress_percentage', 'approved_budget', 'amount_spent', 'ward', 'start_date')
    list_filter = ('status', 'category', 'ward', 'village')
    search_fields = ('project_id', 'name', 'contractor', 'location')
    inlines = [ProjectImageInline, ProjectExpenseInline, ProjectTimelineInline]
    ordering = ('-created_at',)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'stage_type', 'caption', 'created_at')
    list_filter = ('stage_type',)

@admin.register(ProjectExpense)
class ProjectExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'amount', 'spent_date', 'invoice_number')

@admin.register(ProjectTimeline)
class ProjectTimelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'event_date', 'status_reached')
