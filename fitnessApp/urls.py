from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, FitnessEntryViewSet,
    RegisterView, login_view, logout_view,
    HomeTemplateView, AddFitnessEntryTemplateView,AchievementViewSet,LoginTemplateView, RegisterTemplateView, LogoutTemplateView,
    
    block_ip, unblock_ip, list_blocked_ips
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'fitness-entries', FitnessEntryViewSet, basename='fitnessentry')  # <-- Fix applied here
router.register(r'achievements', AchievementViewSet, basename='achievement')
urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', login_view, name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),

    # JWT Token Auth
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Template Views
    path('', HomeTemplateView.as_view(), name='home'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('add-activity/', AddFitnessEntryTemplateView.as_view(), name='add_activity'),
    path('logout/', LogoutTemplateView.as_view(), name='logout'),
    

    # IP Blocking Endpoints
    path('api/ip/block/', block_ip, name='block_ip'),
    path('api/ip/unblock/<str:ip_address>/', unblock_ip, name='unblock_ip'),
    path('api/ip/blocked/', list_blocked_ips, name='list_blocked_ips'),
]

