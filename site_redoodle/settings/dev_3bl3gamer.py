from .base import *
from .mail import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = 'media'
STATIC_ROOT = 'static'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'redoodle.db',
	}
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

