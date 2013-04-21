# coding: utf-8
from django.conf.urls import patterns, url
from .views import index, add_room, add_chain, save_image, like, room, editor

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^add_room/$', add_room, name='add-room'),
    url(r'^add_chain/$', add_chain, name='add-chain'),
    url(r'^save_image/$', save_image, name='save-image'),
    url(r'^like_chain/$', like, name='like-chain'),
    url(r'^(?P<room>\w+)/$', room, name='room'),
    url(r'^(?P<room>\w+)/(?P<chain>\w+)/$', editor, name='editor'),
)
