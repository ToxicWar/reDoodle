# coding: utf-8
from django.conf.urls import patterns, include, url
from .views import index, room, editor
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\w+)/$', room, name='room'),
    url(r'^(\w+)/(\w+)/$', editor, name='editor'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
