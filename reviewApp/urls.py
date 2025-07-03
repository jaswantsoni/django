from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MovieReviewViewSet

from . import views

#import for jwt 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'moviereviews', MovieReviewViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<str:movie_title>/', views.movie_reviews, name='movie_reviews'),
    path('my-reviews/', views.user_reviews, name='user_reviews'),
    path('submit/', views.submit_review, name='submit'),
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),

    
    path('not-verified/', views.not_verified, name='not_verified'),
    #for users that aren't allowed by admin to access certain page, they will be redirected here
    
    path('api/', include(router.urls)),
    
    #JWT Authentication endpoints (ptr: blacklist for refresh in postman)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    #for IP Blocking
    #ip Blocking endpoints
    path('api/ip/block/', views.block_ip, name='block_ip'),
    path('api/ip/unblock/<str:ip_address>/', views.unblock_ip, name='unblock_ip'),
    path('api/ip/blocked/', views.list_blocked_ips, name='list_blocked_ips'),
    path('api/upload/image/', views.upload_image, name='upload_image'),
    path('api/upload/images/', views.upload_multiple_images, name='upload_multiple_images'),
    path('api/delete/image/', views.delete_image, name='delete_image'),
]


