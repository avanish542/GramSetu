from django.shortcuts import render, get_object_or_404
from .models import PanchayatService

def service_list(request):
    services = PanchayatService.objects.filter(is_active=True).prefetch_related('requirements')
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(PanchayatService.objects.prefetch_related('requirements'), pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})
