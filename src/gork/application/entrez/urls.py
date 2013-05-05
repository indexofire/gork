# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'entrez.views',
    url(r'^$', 'index', name='entrez-index'),
    url(r'^term/(?P<slug>[a-zA-Z0-9_-]+)/$', 'term_list', name='entrez-term-list'),
    url(r'^ajax/mark_as_read/$', 'mark_as_read', name='entrez-mark-as-read'),
    url(r'^add/$', 'add_term', name='entrez-add-term'),
    #url(r'^group/$', 'group_list', name='entrez-group'),
    #url(r'^group/(P?<name>\w+)/$', 'group_list', name='entrez-group'),
)
