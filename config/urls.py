from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core & Auth
    path('', include('apps.core.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('', include('apps.village.urls')),
    path('', include('apps.development.urls')),
    path('', include('apps.complaints.urls')),
    path('', include('apps.services.urls')),
    path('', include('apps.applications.urls')),
    path('', include('apps.schemes.urls')),
    path('', include('apps.notices.urls')),
    path('', include('apps.gallery.urls')),
    path('', include('apps.infrastructure.urls')),
    path('', include('apps.feedback.urls')),
    path('', include('apps.notifications.urls')),
    path('', include('apps.dashboard.urls')),

    # REST API Endpoints
    path('api/', include('api.urls')),
]

handler400 = 'apps.core.views.handler400'
handler403 = 'apps.core.views.handler403'
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
