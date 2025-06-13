from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ReviewViewSet

app_name = 'movie'

# API Router setup
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('review/create/', views.create_review, name='create_review'),
    path('api/', include(router.urls)), 
]