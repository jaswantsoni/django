# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app  import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views
# from rest_framework import routers, serializers, viewsets

# admin.site.site_header = "Movie Reviewer Authentication"
# admin.site.site_title = "Movie Review"
# admin.site.index_title = "Welcome! Reviewer"

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #path('', include('testApp.urls')),
#     #path('', include('movieApp.urls')),
#     path('', include('reviewApp.urls')),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviewApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
