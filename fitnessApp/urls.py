from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FitnessEntryViewSet, RegisterView, HomeView, login_view, logout_view

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'fitness-entries', FitnessEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

