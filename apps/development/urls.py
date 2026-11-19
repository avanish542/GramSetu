from django.urls import path
from . import views

app_name = 'development'

urlpatterns = [
    path('development/', views.project_list, name='list'),
    path('development/category/<slug:category_slug>/', views.project_list, name='category_list'),
    path('development/roads/', views.project_list, {'category_slug': 'roads'}, name='roads'),
    path('development/drainage/', views.project_list, {'category_slug': 'drainage'}, name='drainage'),
    path('development/water/', views.project_list, {'category_slug': 'water-supply'}, name='water'),
    path('development/street-lights/', views.project_list, {'category_slug': 'street-lights'}, name='street_lights'),
    path('development/schools/', views.project_list, {'category_slug': 'schools'}, name='schools'),
    path('development/health/', views.project_list, {'category_slug': 'health-facilities'}, name='health'),
    path('development/waste-management/', views.project_list, {'category_slug': 'waste-management'}, name='waste_management'),
    path('development/electricity/', views.project_list, {'category_slug': 'electricity'}, name='electricity'),
    path('development/<int:pk>/', views.project_detail, name='detail'),
    path('budget/', views.budget_transparency, name='budget'),
]
