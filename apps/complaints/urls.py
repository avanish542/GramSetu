from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('complaints/', views.my_complaints, name='my_complaints'),
    path('complaints/create/', views.submit_complaint, name='submit'),
    path('complaints/<int:pk>/', views.complaint_detail, name='detail'),
]
