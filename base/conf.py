# coding: utf-8
from django.conf import settings
from appconf import AppConf

class RedoodleBaseConf(AppConf):
    PATH_ROOMS = 'base/static/room/'

    class Meta:
        prefix = 'BASE'

app_settings = RedoodleBaseConf()