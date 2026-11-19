from django.shortcuts import render
from django.core.paginator import Paginator
from .models import GalleryItem, GalleryCategory

def gallery_list(request):
    items = GalleryItem.objects.filter(is_archived=False)
    category_filter = request.GET.get('category')

    if category_filter:
        items = items.filter(category=category_filter)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,
        'categories': GalleryCategory.choices,
        'selected_category': category_filter,
    }
    return render(request, 'gallery/gallery_list.html', context)
