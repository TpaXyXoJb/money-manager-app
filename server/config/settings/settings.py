import os
from pathlib import Path
from datetime import timedelta

import dj_database_url

BASE_DIR = Path(__file__).parents[2]
SECRET_KEY = '!6xmo&@!7dzw8p6yxjnj&&1lur%4+fs!r2tuzb#6j(64s@m6)*'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ALLOWED_HOSTS = ['*']
SITE_ID = 1

##################################################################
# Debug settings (with docker)
##################################################################

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

##################################################################
# Databases settings (with docker)
##################################################################

DATABASES = {'default': dj_database_url.config()}

##################################################################
# Logging settings
##################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

##################################################################
# Templates, middleware settings
##################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##################################################################
# Password validation settings
##################################################################

if not DEBUG:
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

##################################################################
# Static files settings (CSS, JavaScript, Images)
##################################################################

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
STATICFILES_DIRS = ('static',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

FILE_UPLOAD_PERMISSIONS = 0o777
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777

##################################################################
# REST FRAMEWORK
##################################################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

##################################################################
# Custom user settings
##################################################################

AUTH_USER_MODEL = 'users.User'

##################################################################
# Default auto field settings
##################################################################

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

##################################################################
# Simple jwt settings
##################################################################

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
}

##################################################################
# Swagger settings
##################################################################

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter the token with "Bearer " prefix, e.g., "Bearer <your_token>"',
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

##################################################################
# Debug toolbar settings
##################################################################

if DEBUG:
    from .installed_apps import INSTALLED_APPS


    def show_toolbar(request):
        from django.conf import settings
        return settings.DEBUG


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INSTALLED_APPS += ['debug_toolbar']
