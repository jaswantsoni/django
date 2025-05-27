from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
]
