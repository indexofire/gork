# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from article.views import ArticleList, ArticleDetail


urlpatterns = patterns('article.views',
    #url(r'^$', ArticleList.as_view(), name='article_index'),
    url(r'^$', 'article_index', name='article_index'),
    url(r'^(?P<slug>[a-z0-9_-]+)/$', ArticleDetail.as_view(), name='article_detail'),
)
