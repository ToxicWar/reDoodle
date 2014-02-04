# coding: utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from api.urls import urlpatterns as api_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include(api_urlpatterns)),
    url(r'^my_little_admin/', include(admin.site.urls)),
    url(r'^auth/', include('auth.urls')),
    url(r'', include('redoodle.urls')),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
