from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
]
