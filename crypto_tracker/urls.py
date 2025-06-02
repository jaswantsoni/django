from django.urls import path
from . import views

app_name = 'crypto_tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('coins/', views.coin_list, name='coin_list'),
    path('register/', views.register, name='register'),
    path('create-post/', views.create_post, name='create_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('add-watch/', views.add_watch_entry, name='add_watch_entry'),
    path('add-investment/', views.add_investment, name='add_investment'),
    path('coin/<str:coin_id>/', views.coin_detail, name='coin_detail'),
    path('api/price/<str:coin_id>/', views.get_coin_price, name='get_coin_price'),
] 