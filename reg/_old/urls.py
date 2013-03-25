# coding: utf-8
from django.conf.urls import patterns, url
from views import index, login, logout

urlpatterns = patterns('',
    url(r'^$', index, name='Index'),
    url(r'^login/', login, name='Login'),
    url(r'^logout/', logout, name='Logout'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
