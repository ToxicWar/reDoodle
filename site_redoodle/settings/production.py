# coding: utf-8
from .base import *
import os

DEBUG = True
DATABASES = {}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = '*'

PROJECT_PATH = '/app/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
