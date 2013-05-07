# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^fav/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/$', 'gfavor.views.ajax_fav', name="ajax_fav"),
)
