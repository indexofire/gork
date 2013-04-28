# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from feedz.syndication import PostFeed


urlpatterns = patterns(
    'feedz.views',
    url(r'^$', 'index', name='feed-index'),
    #url('^tag/(?P<tag_value>.+)$', 'tag', name='feed-tag'),
    url(r'^sources/$', 'source_list', name='feed-source-list'),
    #url('^search$', 'search', name='feedzilla_search'),
    url(r'^submit/$', 'submit_blog', name='feedzilla_submit_blog'),
)

'''
urlpatterns += patterns('django.contrib.syndication.views',
    # WTF???
    url(r'^ru/projects/feed$', PostFeed(), name='feedzilla_feed'),
    # depprecated
    url(r'^feeds/posts$', PostFeed(), name='feedzilla_feed'),
    # new
    url(r'^feed/post$', PostFeed(), name='feedzilla_feed'),
)
'''
