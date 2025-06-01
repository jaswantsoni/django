from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='Welcome Page'),
    path('registration/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
]
