# coding: utf-8
from django.conf.urls import patterns, include, url
from .views import index, room, chain
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(\w+)/$', room),
    url(r'^(\w+)/(\w+)/$', chain),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
