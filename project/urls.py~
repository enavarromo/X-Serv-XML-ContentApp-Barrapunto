# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'acorta.views.homePage'),
    url(r'^favicon.ico/$', 'acorta.views.favicon'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'(\d+)', 'acorta.views.Picknew'),
    url(r'.*', 'acorta.views.la404')
)


"""
    # New, for P2
    url(r'^$', 'acorta.views.homePage'),
    url(r'^favicon.ico/$', 'acorta.views.favicon'),
    url(r'(.*)/', 'acorta.views.GetShort'),

    # Old resources
    url(r'^createPage/$', 'acorta.views.createPage'),
    url(r'^mod/$', 'acorta.views.managePages'),
    url(r'^accounts/profile/$', 'acorta.views.redirectHome'),
    url(r'^login$','django.contrib.auth.views.login'),
    url(r'^logout$','django.contrib.auth.views.logout'),
    url(r'^home/$', 'acorta.views.redirectHome'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'(.*)/', 'acorta.views.pickPage'),
"""
