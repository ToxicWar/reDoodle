# coding: utf-8
from django.conf.urls import patterns, url, include
from .redoodle.urls import urlpatterns as redoodle_urlpatterns

urlpatterns = patterns('',
)

urlpatterns += redoodle_urlpatterns
