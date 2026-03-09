from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('map/', views.trending_map, name='home.trending_map'),
    path('api/trending-regions/', views.api_trending_regions, name='home.api_trending_regions'),
]