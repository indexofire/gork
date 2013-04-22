# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import *


urlpatterns = patterns('article.modules.category.views',
    #url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<article>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
    #url(r'^(?P<category_url>[a-z0-9_/-]+/)$', 'article_category', name='article_category'),
    #url(r'^$', 'article_category', name='article_index'),

    url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/(?P<slug>[a-z0-9_-]+)/$', CategoryArticleDetail.as_view(), name="article_detail"),
    url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/$', CategoryArticleList.as_view(), name='article_category'),
    url(r'^$', CategoryArticleList.as_view(), name='article_index'),
)
