# coding: utf-8
from django.conf.urls import patterns, include, url
from base.views import index, room, editor, add_room, add_chain, save_image, like
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^my_little_admin/', include(admin.site.urls)),
    url(r'^add_room/$', add_room, name='add_room'),
    url(r'^add_chain/$', add_chain, name='add_chain'),
    url(r'^save_image/$', save_image, name='save_image'),
    url(r'^reg/', include('reg.urls')),
    url(r'^like_chain/$', like, name='like_chain'),
    url(r'^(?P<room>\w+)/$', room, name='room'),
    url(r'^(?P<room>\w+)/(?P<chain>\w+)/$', editor, name='editor'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
