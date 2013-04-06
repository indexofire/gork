# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from ask.views.main import ask_index, show_post, PostListView


urlpatterns = patterns('',
    url(r'^$', ask_index, name='ask-index'),
    url(r'^q/(?P<id>\d+)/$', show_post, name='ask-detail'),
)
