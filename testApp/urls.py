from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("home/", views.home_view, name="home"),
    path("", views.login_request, name="index"),
]