# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from article.views import ArticleList, ArticleDetail
from article.module.category.views import CategoryArticleList


urlpatterns = patterns(
    'article.views',
    #url(r'^$', ArticleList.as_view(), name='article_index'),
    url(r'^$', 'article_index', name='article_index'),
)

if 'article.module.category' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        'article.views',
        url(r'^category/(?P<category_url>[a-z0-9_-]+)/$', CategoryArticleList.as_view(), name='article_category'),
        url(r'^article/(?P<slug>[a-z0-9_-]+)/$', ArticleDetail.as_view(), name='article_detail'),
    )
else:
    urlpatterns += patterns(
        'article.views',
        url(r'^(?P<slug>[a-z0-9_-]+)/$', ArticleDetail.as_view(), name='article_detail'),
    )
