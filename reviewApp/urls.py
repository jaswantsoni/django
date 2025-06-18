from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MovieReviewViewSet

#import for jwt 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'moviereviews', MovieReviewViewSet)

urlpatterns = [
    path('submit/', views.submit_review, name='submit'),
    path('reviews/', views.review_list, name='review_list'),
    path('api/', include(router.urls)),
    #JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


