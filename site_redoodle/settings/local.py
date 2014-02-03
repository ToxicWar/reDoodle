# coding: utf-8
from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
try:
    VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
except KeyError:
    raise ImproperlyConfigured(
        'This should(actually it shouldn\'t) be used only inside virtual env')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = os.path.join(VIRTUAL_ENV, 'www/media')
STATIC_ROOT = os.path.join(VIRTUAL_ENV, 'www/static')

INSTALLED_APPS += (
    'django_extensions',
)
