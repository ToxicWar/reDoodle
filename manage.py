#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_redoodle.settings")
	
	# import auth.vkauth Ha Ha Ha, No
	
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
