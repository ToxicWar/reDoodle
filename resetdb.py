#!/usr/bin/python
from redoodle.settings import DATABASES
from os import system

cmd = "rm " + DATABASES['default']['NAME'] + ";"\
      "python manage.py syncdb;" +\
      "python manage.py migrate;" +\
      "python manage.py loaddata */fixtures/*.json;"
system(cmd)

