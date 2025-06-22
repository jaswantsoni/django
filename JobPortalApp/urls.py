from django.urls import path
from JobPortalApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('job-posts', views.JobPostViewSet)
router.register('applications', views.ApplicationViewSet)

# Frontend URLs
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('jobs/', views.JobPostListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobPostDetailView.as_view(), name='job-detail'),
    path('jobs/create/', views.JobPostCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/apply/', views.ApplicationCreateView.as_view(), name='apply-job'),
]

urlpatterns += router.urls