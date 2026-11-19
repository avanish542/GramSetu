from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from apps.development.models import DevelopmentProject, ProjectStatus
from apps.complaints.models import Complaint, ComplaintStatus
from apps.applications.models import ServiceApplication, ApplicationStatus
from apps.accounts.models import User, UserRole
from apps.notices.models import Notice

@login_required
def index(request):
    if request.user.is_superadmin:
        return redirect('dashboard:super_admin_dashboard')
    elif request.user.is_panchayat_admin:
        return redirect('dashboard:panchayat_dashboard')
    return redirect('dashboard:villager_dashboard')


@login_required
def villager_dashboard(request):
    my_applications = ServiceApplication.objects.filter(applicant=request.user).select_related('service')[:5]
    my_complaints = Complaint.objects.filter(user=request.user).select_related('category')[:5]
    notifications = request.user.notifications.filter(is_read=False)[:5]

    pending_apps_count = ServiceApplication.objects.filter(
        applicant=request.user,
        status__in=[ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_VERIFICATION]
    ).count()
    
    approved_apps_count = ServiceApplication.objects.filter(
        applicant=request.user,
        status=ApplicationStatus.APPROVED
    ).count()

    pending_complaints_count = Complaint.objects.filter(
        user=request.user
    ).exclude(status__in=[ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]).count()

    resolved_complaints_count = Complaint.objects.filter(
        user=request.user,
        status=ComplaintStatus.RESOLVED
    ).count()

    context = {
        'my_applications': my_applications,
        'my_complaints': my_complaints,
        'notifications': notifications,
        'pending_apps_count': pending_apps_count,
        'approved_apps_count': approved_apps_count,
        'pending_complaints_count': pending_complaints_count,
        'resolved_complaints_count': resolved_complaints_count,
    }
    return render(request, 'dashboard/villager.html', context)


@login_required
def panchayat_dashboard(request):
    if not request.user.is_panchayat_admin:
        return redirect('dashboard:villager_dashboard')

    total_villagers = User.objects.filter(role=UserRole.VILLAGER).count()
    
    projects = DevelopmentProject.objects.all()
    total_projects = projects.count()
    completed_projects = projects.filter(status=ProjectStatus.COMPLETED).count()
    ongoing_projects = projects.filter(status=ProjectStatus.IN_PROGRESS).count()
    pending_projects = projects.filter(status=ProjectStatus.PLANNED).count()

    total_budget = projects.aggregate(total=Sum('approved_budget'))['total'] or 0
    total_spent = projects.aggregate(total=Sum('amount_spent'))['total'] or 0

    complaints = Complaint.objects.all()
    total_complaints = complaints.count()
    pending_complaints = complaints.exclude(status__in=[ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED]).count()
    resolved_complaints = complaints.filter(status=ComplaintStatus.RESOLVED).count()

    applications = ServiceApplication.objects.all()
    pending_verification_apps = applications.filter(
        status__in=[ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_VERIFICATION]
    ).count()

    recent_complaints = Complaint.objects.select_related('user', 'category', 'ward')[:5]
    recent_applications = ServiceApplication.objects.select_related('applicant', 'service')[:5]

    context = {
        'total_villagers': total_villagers,
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'ongoing_projects': ongoing_projects,
        'pending_projects': pending_projects,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'pending_verification_apps': pending_verification_apps,
        'recent_complaints': recent_complaints,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/panchayat.html', context)


@login_required
def super_admin_dashboard(request):
    if not request.user.is_superadmin:
        return redirect('dashboard:index')

    total_users = User.objects.count()
    total_villagers = User.objects.filter(role=UserRole.VILLAGER).count()
    total_admins = User.objects.filter(role=UserRole.PANCHAYAT_ADMIN).count()
    total_projects = DevelopmentProject.objects.count()
    total_complaints = Complaint.objects.count()
    total_applications = ServiceApplication.objects.count()

    context = {
        'total_users': total_users,
        'total_villagers': total_villagers,
        'total_admins': total_admins,
        'total_projects': total_projects,
        'total_complaints': total_complaints,
        'total_applications': total_applications,
    }
    return render(request, 'dashboard/super_admin.html', context)
