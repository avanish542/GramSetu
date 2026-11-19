from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Notice, NoticeCategory

def notice_list(request):
    notices = Notice.objects.filter(is_published=True).select_related('published_by')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')

    if category_filter:
        notices = notices.filter(category=category_filter)
    if search_query:
        notices = notices.filter(title__icontains=search_query) | notices.filter(description__icontains=search_query)

    paginator = Paginator(notices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notices': page_obj,
        'categories': NoticeCategory.choices,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'notices/notice_list.html', context)

def notice_detail(request, pk):
    notice = get_object_or_404(Notice.objects.select_related('published_by'), pk=pk)
    return render(request, 'notices/notice_detail.html', {'notice': notice})
