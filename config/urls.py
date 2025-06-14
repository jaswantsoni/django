from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import college
from college.views import BankingViewSet, CollegeViewSet, UserViewSetCollege
from skillSwap.views import SkillViewSet, SkillSessionViewSet, RatingViewSet, UserViewSet
from skillSwap import views  # <-- we will create a frontend view

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'sessions', SkillSessionViewSet, basename='sessions')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'users', UserViewSet, basename='users')

college = DefaultRouter()
college.register(r'users', UserViewSetCollege)
college.register(r'colleges', CollegeViewSet)
college.register(r'bankings', BankingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('users/', views.users_page, name='users_page'),
    path('skills/', views.skills_page, name='skills_page'),
    path('sessions/', views.sessions_page, name='sessions_page'),
    path('college/', include(college.urls)),

    path('api/skill-swap/', include(router.urls)),
]
