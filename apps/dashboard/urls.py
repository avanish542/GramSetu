from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('dashboard/villager/', views.villager_dashboard, name='villager_dashboard'),
    path('panchayat/dashboard/', views.panchayat_dashboard, name='panchayat_dashboard'),
    path('super-admin/dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
]
