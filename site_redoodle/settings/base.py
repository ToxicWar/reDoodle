# coding: utf-8
try:
    from .mail import *
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        'I need a POP3 server config for sending emails, '+
        'so please create a mail.py file with something like:\n'+
        '  EMAIL_HOST = \'smtp.yandex.ru\'\n'+
        '  EMAIL_HOST_USER = \'TheGreatAndPowerfulTrixie@yandex.ru\'\n'+
        '  EMAIL_HOST_PASSWORD = \'password\'\n'+
        '  EMAIL_PORT = 587\n'+
        '  EMAIL_USE_TLS = True')

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

SECRET_KEY = 'yy3d&amp;rmb$g$8ucut=9(@g=qi2%*ro552^7$xzddj_wif_0f)sg'

MIDDLEWARE_CLASSES = (
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'site_redoodle.urls'

WSGI_APPLICATION = 'site_redoodle.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'redoodle',
    'auth',

    'rest_framework',
    'south',
)

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
    'auth.backends.LoginBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

#from django.core.urlresolvers import reverse_lazy
LOGIN_URL = "/auth/login"

