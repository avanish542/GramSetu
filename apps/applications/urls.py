from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('applications/', views.my_applications, name='my_applications'),
    path('applications/apply/<int:service_id>/', views.apply_for_service, name='apply'),
    path('applications/<int:pk>/', views.application_detail, name='detail'),
    path('applications/document/<int:doc_id>/download/', views.download_document, name='download_document'),
]
