# coding: utf-8
from django.conf.urls import patterns, include, url
from .views import hello, current_datetime, room, chain
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', hello, name='hello'),
    url(r'^datatime/$', current_datetime),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^([A-Za-z]+)/$', room),
    url(r'^([A-Za-z]+)/([A-Za-z]+)/$', chain),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
