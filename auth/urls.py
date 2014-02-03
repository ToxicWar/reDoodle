# coding: utf-8
from django.conf.urls import patterns, url
from views import login_view, logout, register_view, mail_confirm_view, rmf

urlpatterns = patterns('',
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^rmf/$', rmf, name='rmf'),
    url(r'^register/$', register_view, name='register'),
    url(r'^mail_confirm/$', mail_confirm_view, name='mail_confirm'),
    #url(r'^reg_complete/', reg_complete_view, name='reg_complete'),
)
