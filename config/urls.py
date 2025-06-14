from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skillSwap.views import SkillViewSet, SkillSessionViewSet, RatingViewSet, UserViewSet
from skillSwap import views  # <-- we will create a frontend view

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'sessions', SkillSessionViewSet, basename='sessions')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('users/', views.users_page, name='users_page'),
    path('skills/', views.skills_page, name='skills_page'),
    path('sessions/', views.sessions_page, name='sessions_page'),
    
    path('api/skill-swap/', include(router.urls)),
]
