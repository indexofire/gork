# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('gfavor.views',
    #url(r'^fav/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/$', 'ajax_fav', name="ajax_fav"),
    #url(r'^fav/(?P<ctype_id>\d+)/(?P<obj_id>\d+)/$', 'ajax_add_favorite', name="ajax_fav"),
    url(r'^fav$', 'ajax_add_favorite', name="ajax_fav"),
    #url(r'^add$', 'ajax_add_favorite', name="favorite_ajax_add"),
    #url(r'^remove$', 'ajax_remove_favorite', name="favorite_ajax_remove"),
)
