from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, FitnessEntryViewSet,
    RegisterView, login_view, logout_view,
    HomeTemplateView, LoginTemplateView, RegisterTemplateView, LogoutTemplateView,
    AddFitnessEntryTemplateView 
)
router = DefaultRouter()
router.register(r'users', UserViewSet) 
router.register(r'fitness-entries', FitnessEntryViewSet) 

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', login_view, name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),
    path('', HomeTemplateView.as_view(), name='home'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('add-activity/', AddFitnessEntryTemplateView.as_view(), name='add_activity'),
    
path('logout/', LogoutTemplateView.as_view(), name='logout'),
]


