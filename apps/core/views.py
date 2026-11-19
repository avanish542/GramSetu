from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from apps.development.models import DevelopmentProject, ProjectStatus
from apps.complaints.models import Complaint, ComplaintStatus
from apps.schemes.models import GovernmentScheme
from apps.notices.models import Notice
from apps.village.models import Village

def home(request):
    """
    Homepage displaying dynamic dynamic village statistics, featured projects, pinned notices,
    and hero call to actions. Aggregate statistics are cached in Redis / LocMem cache.
    """
    stats = cache.get('homepage_stats')
    if not stats:
        village = Village.objects.first()
        total_villagers = village.population if village else 12500
        total_projects = DevelopmentProject.objects.count()
        completed_projects = DevelopmentProject.objects.filter(status=ProjectStatus.COMPLETED).count()
        ongoing_projects = DevelopmentProject.objects.filter(status=ProjectStatus.IN_PROGRESS).count()
        resolved_complaints = Complaint.objects.filter(status=ComplaintStatus.RESOLVED).count()
        active_schemes = GovernmentScheme.objects.filter(is_active=True).count()

        stats = {
            'total_villagers': total_villagers,
            'total_projects': total_projects,
            'completed_projects': completed_projects,
            'ongoing_projects': ongoing_projects,
            'resolved_complaints': resolved_complaints,
            'active_schemes': active_schemes,
        }
        cache.set('homepage_stats', stats, 300) # Cache for 5 minutes

    featured_projects = DevelopmentProject.objects.select_related('category', 'ward').prefetch_related('images')[:6]
    latest_notices = Notice.objects.filter(is_published=True)[:4]

    context = {
        'stats': stats,
        'featured_projects': featured_projects,
        'latest_notices': latest_notices,
    }
    return render(request, 'core/home.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def health_check(request):
    """GET /health/ endpoint"""
    return JsonResponse({"status": "healthy", "service": "GramSetu V2"})

def ready_check(request):
    """GET /ready/ endpoint verifying Database readiness"""
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    if db_ok:
        return JsonResponse({"status": "ready", "database": "connected"})
    return JsonResponse({"status": "unready", "database": "disconnected"}, status=503)

# Custom Error Handlers
def handler400(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def handler403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)
