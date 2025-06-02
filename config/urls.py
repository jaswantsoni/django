"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from django.conf.urls.static import static
# from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path("test/", include("akshat.urls")),
#     path("skill-swap/", include("skillSwap.urls")),
#     path('accounts', include('django.contrib.auth.urls')),
    
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skillSwap.views import (SkillViewSet, SkillSessionViewSet, RatingViewSet, UserViewSet, )


router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'sessions', SkillSessionViewSet, basename='sessions')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
path('admin/', admin.site.urls),
path('skill-swap/', include(router.urls)),
]