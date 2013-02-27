# coding: utf-8
from django.conf.urls import patterns, url
from .views import graphics_editor

urlpatterns = patterns('',
    url(r'^graphics_editor/', graphics_editor, name='graphics_editor'),
)