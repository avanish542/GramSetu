from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import (
    DevelopmentProjectViewSet, ComplaintViewSet, PanchayatServiceViewSet,
    ServiceApplicationViewSet, GovernmentSchemeViewSet, NoticeViewSet,
    GalleryViewSet, InfrastructureViewSet
)

router = DefaultRouter()
router.register(r'projects', DevelopmentProjectViewSet, basename='project')
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'services', PanchayatServiceViewSet, basename='service')
router.register(r'applications', ServiceApplicationViewSet, basename='application')
router.register(r'schemes', GovernmentSchemeViewSet, basename='scheme')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'infrastructure', InfrastructureViewSet, basename='infrastructure')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]
