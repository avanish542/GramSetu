from django.urls import path
from . import views

app_name = 'schemes'

urlpatterns = [
    path('schemes/', views.scheme_list, name='list'),
    path('schemes/<int:pk>/', views.scheme_detail, name='detail'),
]
