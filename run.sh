#!/bin/bash
dir="redoodle/base/static/room"
if [ ! -d $dir ]; then
mkdir $dir
fi
python manage.py runserver 0.0.0.0:9000
