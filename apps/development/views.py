from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from .models import DevelopmentProject, ProjectCategory, ProjectStatus

def project_list(request, category_slug=None):
    category = None
    categories = ProjectCategory.objects.all()
    projects = DevelopmentProject.objects.select_related('category', 'ward').all()

    if category_slug:
        category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=category)

    # Filtering
    status_filter = request.GET.get('status')
    ward_filter = request.GET.get('ward')
    search_query = request.GET.get('q')

    if status_filter:
        projects = projects.filter(status=status_filter)
    if ward_filter:
        projects = projects.filter(ward_id=ward_filter)
    if search_query:
        projects = projects.filter(name__icontains=search_query)

    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj,
        'category': category,
        'categories': categories,
        'selected_status': status_filter,
        'search_query': search_query,
        'status_choices': ProjectStatus.choices,
    }
    return render(request, 'development/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(
        DevelopmentProject.objects.select_related('category', 'ward', 'village')
        .prefetch_related('images', 'expenses', 'timeline_events', 'feedback_entries__user'),
        pk=pk
    )

    user_has_submitted_feedback = False
    if request.user.is_authenticated:
        user_has_submitted_feedback = project.feedback_entries.filter(user=request.user).exists()

    avg_rating = None
    if project.feedback_entries.exists():
        avg_rating = project.feedback_entries.aggregate(avg=Sum('rating'))['avg'] / project.feedback_entries.count()

    context = {
        'project': project,
        'before_images': project.images.filter(stage_type='BEFORE'),
        'during_images': project.images.filter(stage_type='DURING'),
        'after_images': project.images.filter(stage_type='AFTER'),
        'expenses': project.expenses.all(),
        'timeline': project.timeline_events.all(),
        'feedback_list': project.feedback_entries.all(),
        'user_has_submitted_feedback': user_has_submitted_feedback,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
    }
    return render(request, 'development/project_detail.html', context)


def budget_transparency(request):
    projects = DevelopmentProject.objects.all()
    
    total_budget = projects.aggregate(total=Sum('approved_budget'))['total'] or 0
    total_spent = projects.aggregate(total=Sum('amount_spent'))['total'] or 0
    remaining_budget = max(0, total_budget - total_spent)
    
    total_count = projects.count()
    completed_count = projects.filter(status=ProjectStatus.COMPLETED).count()
    ongoing_count = projects.filter(status=ProjectStatus.IN_PROGRESS).count()

    category_data = (
        DevelopmentProject.objects.values('category__name')
        .annotate(total_budget=Sum('approved_budget'), total_spent=Sum('amount_spent'))
        .order_by('-total_budget')
    )

    context = {
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'total_count': total_count,
        'completed_count': completed_count,
        'ongoing_count': ongoing_count,
        'category_data': list(category_data),
    }
    return render(request, 'development/budget.html', context)
