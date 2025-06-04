from django.urls import path
from JobPortalApp import views
from rest_framework.routers import DefaultRouter


urlpatterns = [

]
router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('job-posts', views.JobPostViewSet)
router.register('applications', views.ApplicationViewSet)

urlpatterns += router.urls