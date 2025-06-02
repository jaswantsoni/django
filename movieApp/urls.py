from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('review/create/', views.create_review, name='create_review'), 
    path('filter/', views.filter_movies, name='filter_movies'),
]