# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url('^json/get/$', 'gnotify.views.get_notifications', name='json_get'),
    url('^json/get/(?P<latest_id>\d+)/$', 'gnotify.views.get_notifications', name='json_get'),
    url('^json/mark-read/$', 'gnotify.views.mark_read', name='json_mark_read_base'),
    url('^json/mark-read/(\d+)/$', 'gnotify.views.mark_read', name='json_mark_read'),
    url('^json/mark-read/(?P<id_lte>\d+)/(?P<id_gte>\d+)/$', 'gnotify.views.mark_read', name='json_mark_read'),
    url('^goto/(?P<notification_id>\d+)/$', 'gnotify.views.goto', name='goto'),
    url('^goto/$', 'gnotify.views.goto', name='goto_base'),
)


def get_pattern(app_name="notify", namespace="notify"):
    """Every url resolution takes place as "notify:view_name".
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace
