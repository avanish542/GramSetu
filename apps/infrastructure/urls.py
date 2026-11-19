from django.urls import path
from . import views

app_name = 'infrastructure'

urlpatterns = [
    path('map/', views.village_map, name='map'),
]
