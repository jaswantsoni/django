from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MovieReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'moviereviews', MovieReviewViewSet)

urlpatterns = [
    path('submit/', views.submit_review, name='submit'),
    path('reviews/', views.review_list, name='review_list'),
    path('api/', include(router.urls)),
]
