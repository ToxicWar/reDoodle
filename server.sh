#!/bin/bash
export DJANGO_SETTINGS_MODULE=site_redoodle.settings.production
gunicorn site_redoodle.wsgi -b 0.0.0.0:$PORT