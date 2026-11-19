from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Village, Ward, VillageInfo, VillageCondition, RelatedPanchayat

def about_village(request):
    village = Village.objects.first()
    info = VillageInfo.objects.filter(village=village).first() if village else None
    wards = Ward.objects.filter(village=village) if village else []
    conditions = VillageCondition.objects.filter(village=village) if village else []
    related_panchayats = RelatedPanchayat.objects.all()

    context = {
        'village': village,
        'info': info,
        'wards': wards,
        'conditions': conditions,
        'related_panchayats': related_panchayats,
    }
    return render(request, 'village/about.html', context)


def condition_dashboard(request):
    village = Village.objects.first()
    all_conditions = VillageCondition.objects.select_related('village', 'related_panchayat').all()
    
    total_assessed_conditions = all_conditions.count()
    categories_assessed_count = all_conditions.values('category').distinct().count()
    
    primary_village_count = 1 if village else 0
    rel_panchayats_assessed = RelatedPanchayat.objects.filter(conditions__isnull=False).distinct().count()
    total_locations_assessed = primary_village_count + rel_panchayats_assessed
    
    status_counts = {
        'GOOD': all_conditions.filter(condition_status='GOOD').count(),
        'MODERATE': all_conditions.filter(condition_status='MODERATE').count(),
        'NEEDS_ATTENTION': all_conditions.filter(condition_status='NEEDS_ATTENTION').count(),
        'CRITICAL': all_conditions.filter(condition_status='CRITICAL').count(),
        'UNKNOWN': all_conditions.filter(condition_status='UNKNOWN').count(),
    }
    
    verified_count = all_conditions.filter(verified=True).count()
    demo_count = all_conditions.filter(verified=False).count()
    
    categories_list = [c[0] for c in VillageCondition.CATEGORY_CHOICES]
    category_summary = []
    for cat in categories_list:
        cat_conds = all_conditions.filter(category=cat)
        if cat_conds.exists():
            category_summary.append({
                'category': cat,
                'total': cat_conds.count(),
                'good': cat_conds.filter(condition_status='GOOD').count(),
                'moderate': cat_conds.filter(condition_status='MODERATE').count(),
                'needs_attention': cat_conds.filter(condition_status='NEEDS_ATTENTION').count(),
                'critical': cat_conds.filter(condition_status='CRITICAL').count(),
                'unknown': cat_conds.filter(condition_status='UNKNOWN').count(),
                'items': cat_conds,
            })
            
    location_matrix = []
    if village:
        v_conds = {c.category: c for c in all_conditions.filter(village=village)}
        location_matrix.append({
            'name': f"{village.name} (Primary GP)",
            'type': 'Primary Gram Panchayat',
            'conditions_map': v_conds,
        })
        
    for rp in RelatedPanchayat.objects.all():
        rp_conds = {c.category: c for c in all_conditions.filter(related_panchayat=rp)}
        if rp_conds:
            location_matrix.append({
                'name': rp.name,
                'type': rp.get_category_display(),
                'conditions_map': rp_conds,
            })

    context = {
        'village': village,
        'total_assessed_conditions': total_assessed_conditions,
        'categories_assessed_count': categories_assessed_count,
        'total_locations_assessed': total_locations_assessed,
        'status_counts': status_counts,
        'verified_count': verified_count,
        'demo_count': demo_count,
        'category_summary': category_summary,
        'categories_list': categories_list,
        'location_matrix': location_matrix,
        'all_conditions': all_conditions,
    }
    return render(request, 'village/conditions.html', context)
