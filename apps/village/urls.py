from django.urls import path
from . import views

app_name = 'village'

urlpatterns = [
    path('about-village/', views.about_village, name='about'),
    path('village-conditions/', views.condition_dashboard, name='conditions'),
]
