# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('api.redoodle.views',
    url('^rooms/$', 'room_list', name='ApiRoomList'),
    url('^room/(?P<pk>[0-9]+)/$', 'room_detail', name='ApiRoomDetail'),
    url('^chains/$', 'chain_list', name='ApiChainList'),
    url('^chain/(?P<pk>[0-9]+)/$', 'chain_detail', name='ApiChainDetail'),
)
