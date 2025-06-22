from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9!#4fd7gk5qbrv^3hknj2dnl816eunwwg_pb14cp!vp-3yl&0@'

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'fitnessApp.User'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

INSTALLED_APPS = [
    'fitnessApp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    }
SIMPLE_JWT = {
    # Token lifetime settings
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Changed from 60 to 30 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Changed from 1 to 7 days
   
    # Token refresh settings
    'ROTATE_REFRESH_TOKENS': True,  # Generate new refresh token when refreshing
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old refresh tokens
   
    # Signature settings
    'ALGORITHM': 'HS512',  # Changed from HS256 to HS512 for stronger signature
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
   
    # Token header settings
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),  # Accept both Bearer and JWT in header
   
    # Token payload settings
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
   
    # Additional settings
    'JTI_CLAIM': 'jti',  # JWT ID claim
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}
 
 

MIDDLEWARE = [
   
    'fitnessApp.middleware.LogAndBlockIPMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
BLOCKED_IPS = [
    '192.168.1.100',
    '10.0.0.1',
    # Add more IPs as needed
]
CORS_ALLOWED_ORIGINS=[
    
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'fitnessApp', 'templates', 'registration')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION =  'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness_app',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',   
        'PORT': '3306', 
    }
}

    

    


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'