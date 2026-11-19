from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import GovernmentScheme, SchemeCategory

def scheme_list(request):
    schemes = GovernmentScheme.objects.filter(is_active=True)
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')

    if category_filter:
        schemes = schemes.filter(category=category_filter)
    if search_query:
        schemes = schemes.filter(name__icontains=search_query) | schemes.filter(benefits__icontains=search_query)

    paginator = Paginator(schemes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'schemes': page_obj,
        'categories': SchemeCategory.choices,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'schemes/scheme_list.html', context)

def scheme_detail(request, pk):
    scheme = get_object_or_404(GovernmentScheme, pk=pk)
    return render(request, 'schemes/scheme_detail.html', {'scheme': scheme})
