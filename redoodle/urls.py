# coding: utf-8
from django.conf.urls import patterns, include, url
from base.views import index, room, editor, add_room, add_chain, save_image, like
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^my_little_admin/', include(admin.site.urls)),
    url(r'^reg/', include('reg.urls')),
    url(r'', include('base.urls'))
)
