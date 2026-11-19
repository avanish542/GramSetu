from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    DevelopmentProjectSerializer, ComplaintSerializer, PanchayatServiceSerializer,
    ServiceApplicationSerializer, GovernmentSchemeSerializer, NoticeSerializer,
    GalleryItemSerializer, InfrastructureItemSerializer
)
from apps.development.models import DevelopmentProject
from apps.complaints.models import Complaint
from apps.services.models import PanchayatService
from apps.applications.models import ServiceApplication
from apps.schemes.models import GovernmentScheme
from apps.notices.models import Notice
from apps.gallery.models import GalleryItem
from apps.infrastructure.models import InfrastructureItem


class DevelopmentProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DevelopmentProject.objects.select_related('category', 'ward').prefetch_related('images').all()
    serializer_class = DevelopmentProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'ward']
    search_fields = ['name', 'description', 'contractor', 'location']
    ordering_fields = ['created_at', 'start_date', 'approved_budget', 'progress_percentage']


class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'category', 'ward']
    search_fields = ['ticket_number', 'title', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.is_panchayat_admin:
            return Complaint.objects.select_related('user', 'category', 'ward').all()
        return Complaint.objects.select_related('category', 'ward').filter(user=user)

    def perform_create(self, serializer):
        from django.utils import timezone
        from apps.village.models import Village
        
        year = timezone.now().year
        count = Complaint.objects.count() + 1
        ticket = f"CMP-{year}-{count:04d}"
        serializer.save(user=self.request.user, ticket_number=ticket, village=Village.objects.first())


class PanchayatServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PanchayatService.objects.filter(is_active=True)
    serializer_class = PanchayatServiceSerializer
    search_fields = ['name', 'description', 'category']


class ServiceApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'service']
    search_fields = ['application_number', 'applicant_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_panchayat_admin:
            return ServiceApplication.objects.select_related('applicant', 'service').all()
        return ServiceApplication.objects.select_related('service').filter(applicant=user)


class GovernmentSchemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GovernmentScheme.objects.filter(is_active=True)
    serializer_class = GovernmentSchemeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description', 'benefits']


class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.filter(is_published=True)
    serializer_class = NoticeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_pinned']
    search_fields = ['title', 'description']


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryItem.objects.filter(is_archived=False)
    serializer_class = GalleryItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class InfrastructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InfrastructureItem.objects.select_related('ward').all()
    serializer_class = InfrastructureItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'status', 'ward']
    search_fields = ['name', 'description']
