from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('feedback/submit/<int:project_id>/', views.submit_feedback, name='submit'),
]
