# coding: utf-8
from django.conf.urls import patterns, url
from views import login, logout, register

urlpatterns = patterns('',
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^register/', register, name='register'),
    #url(r'^reg_complete/', reg_complete_view, name='reg_complete'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
