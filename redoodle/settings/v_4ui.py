print "4ui settings file"

from base import *

import os

from django.core.exceptions import ImproperlyConfigured
try:
    VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
except KeyError:
    raise ImproperlyConfigured('This should be used only inside virtual env')

DATABASES['default']['NAME'] = os.path.join(VIRTUAL_ENV, 'redoodle.db')
