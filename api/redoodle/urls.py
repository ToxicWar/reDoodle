# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('api.redoodle.views',
    url('^chains/$', 'chain_list', name='ApiChainList'),
)
