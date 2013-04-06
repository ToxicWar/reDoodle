# coding: utf-8
from .base import *
import os
from django.core.exceptions import ImproperlyConfigured
try:
    VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
except KeyError:
    raise ImproperlyConfigured('This should be used only inside virtual env')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VIRTUAL_ENV, 'redoodle.db'),
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_ROOT = os.path.join(VIRTUAL_ENV, 'www/media')
STATIC_ROOT = os.path.join(VIRTUAL_ENV, 'www/static')
