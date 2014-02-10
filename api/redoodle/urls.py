# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('api.redoodle.views',
    url('^rooms/$', 'room_list', name='ApiRoomList'),
    url('^rooms/(?P<pk>[0-9]+)/$', 'room_detail', name='ApiRoomDetail'),
    url('^chains/$', 'chain_list', name='ApiChainList'),
    url('^chains/(?P<pk>[0-9]+)/$', 'chain_detail', name='ApiChainDetail'),
    url('^image/ban/(?P<pk>[0-9]+)/$', 'image_ban_view', name='ApiImageBanView'),
)
