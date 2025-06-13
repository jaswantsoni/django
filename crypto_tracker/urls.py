from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import WatchEntryViewSet, PostViewSet, InvestmentViewSet, UserViewSet

app_name = 'crypto_tracker'

router = DefaultRouter()
router.register(r'watch-entries', WatchEntryViewSet, basename='watch-entry')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'investments', InvestmentViewSet, basename='investment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
   
    path('', views.HomeView.as_view(), name='home'),
    path('coins/', views.CoinListView.as_view(), name='coin_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create-post/', views.CreatePostView.as_view(), name='create_post'),
    path('like-post/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('add-watch/', views.AddWatchEntryView.as_view(), name='add_watch_entry'),
    path('add-investment/', views.AddInvestmentView.as_view(), name='add_investment'),
    path('coin/<slug:coin_id>/', views.CoinDetailView.as_view(), name='coin_detail'), # Using slug for coin_id
    path('api/price/<str:coin_id>/', views.GetCoinPriceView.as_view(), name='get_coin_price'),
    path('api/', include(router.urls)),
] 