"""
Django settings for cosateca project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import json

with open('cosateca/config.json') as f:
    SECRETS = json.load(f)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'CosatecaApp',
    'chat',
    'django_minio_backend',
    #'django_minio_backend.apps.DjangoMinioBackendConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'cosateca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'cosateca.asgi.application'

# CHANNELS_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     }
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(SECRETS['HOST_REDIS'], 6379)],
        },
    },
}

WSGI_APPLICATION = 'cosateca.wsgi.application'

# Configuracion MinIO
MINIO_CONSISTENCY_CHECK_ON_START = False
from datetime import timedelta
from typing import List, Tuple

MINIO_ENDPOINT = SECRETS['MINIO_ENDPOINT']
MINIO_EXTERNAL_ENDPOINT = SECRETS['MINIO_EXTERNAL_ENDPOINT']
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False  # Default is same as MINIO_USE_HTTPS
MINIO_REGION = 'us-east-1'  # Default is set to None
MINIO_ACCESS_KEY = SECRETS['MINIO_ACCESS_KEY']
MINIO_SECRET_KEY = SECRETS['MINIO_SECRET_KEY']
MINIO_USE_HTTPS = False
MINIO_URL_EXPIRY_HOURS = timedelta(days=7)  # Default is 7 days (longest) if not defined
MINIO_PRIVATE_BUCKETS = [
   'django-backend-dev-private',
]
MINIO_PUBLIC_BUCKETS = [
   'django-backend-dev-public',
]
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []
MINIO_MEDIA_FILES_BUCKET = 'my-media-files-bucket'  # replacement for MEDIA_ROOT
# MINIO_STATIC_FILES_BUCKET = 'my-static-files-bucket'  # replacement for STATIC_ROOT
MINIO_BUCKET_CHECK_ON_SAVE = True  # Default: True // Creates bucket if missing, then save

# Custom HTTP Client (OPTIONAL)
import os
import certifi
import urllib3
timeout = timedelta(minutes=5).seconds
ca_certs = os.environ.get('SSL_CERT_FILE') or certifi.where()
MINIO_HTTP_CLIENT: urllib3.poolmanager.PoolManager = urllib3.PoolManager(
    timeout=urllib3.util.Timeout(connect=timeout, read=timeout),
    maxsize=10,
    cert_reqs='CERT_REQUIRED',
    ca_certs=ca_certs,
    retries=urllib3.Retry(
        total=5,
        backoff_factor=0.2,
        status_forcelist=[500, 502, 503, 504]
    )
)

DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'
MINIO_MEDIA_FILES_BUCKET = 'my-media-files-bucket'
MINIO_PUBLIC_BUCKETS.append(MINIO_MEDIA_FILES_BUCKET)
MEDIA_URL = ''

# Databases
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': SECRETS['ENGINE'],
        'NAME': SECRETS['NAME'],
        'USER': SECRETS['USER'],
        'PASSWORD': SECRETS['PASSWORD'],
        'HOST': SECRETS['HOST'],
        'PORT': SECRETS['PORT'],
        'OPTIONS': {
            "use_pure": True
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

import os.path  
import sys

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
