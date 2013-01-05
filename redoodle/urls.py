# coding: utf-8
from django.conf.urls import patterns, include, url
from redoodle.base.views import index, room, editor
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\w+)/$', room, name='room'),
    url(r'^(\w+)/(\w+)/$', editor, name='editor'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
