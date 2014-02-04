# coding: utf-8
from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reDoodle',
        'USER': 'redoodle',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}
