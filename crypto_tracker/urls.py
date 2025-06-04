from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import WatchEntryViewSet, PostViewSet, InvestmentViewSet

app_name = 'crypto_tracker'

router = DefaultRouter()
router.register(r'watch-entries', WatchEntryViewSet, basename='watch-entry')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'investments', InvestmentViewSet, basename='investment')

urlpatterns = [
    # Regular views
    path('', views.home, name='home'),
    path('coins/', views.coin_list, name='coin_list'),
    path('register/', views.register, name='register'),
    path('create-post/', views.create_post, name='create_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('add-watch/', views.add_watch_entry, name='add_watch_entry'),
    path('add-investment/', views.add_investment, name='add_investment'),
    path('coin/<str:coin_id>/', views.coin_detail, name='coin_detail'),
    path('api/price/<str:coin_id>/', views.get_coin_price, name='get_coin_price'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 