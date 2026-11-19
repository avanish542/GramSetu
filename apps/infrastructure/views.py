import json
from django.shortcuts import render
from .models import InfrastructureItem, InfraCategory

def village_map(request):
    items = InfrastructureItem.objects.select_related('ward', 'village').all()
    categories = InfraCategory.choices
    
    valid_markers = []
    unmapped_count = 0
    
    for item in items:
        try:
            lat = float(item.latitude) if item.latitude is not None else None
            lng = float(item.longitude) if item.longitude is not None else None
        except (ValueError, TypeError):
            lat, lng = None, None
            
        if lat is not None and lng is not None and lat != 0 and lng != 0:
            valid_markers.append({
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'category_display': item.get_category_display(),
                'description': item.description,
                'lat': lat,
                'lng': lng,
                'ward': item.ward.ward_name if item.ward else 'N/A',
                'status': item.get_status_display(),
                'image_url': item.image.url if item.image else None,
            })
        else:
            unmapped_count += 1

    context = {
        'markers_json': json.dumps(valid_markers),
        'total_items_count': items.count(),
        'mapped_count': len(valid_markers),
        'unmapped_count': unmapped_count,
        'categories': categories,
    }
    return render(request, 'infrastructure/map.html', context)
