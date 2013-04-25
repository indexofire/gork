# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from gmessage.views import *


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url="inbox/"), name='gmessage-redirect'),
    url(r'^inbox/$', inbox, name='gmessage-inbox'),
    url(r'^outbox/$', outbox, name='gmessage-outbox'),
    url(r'^compose/$', compose, name='gmessage-compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='gmessage-compose-to'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='gmessage-reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, name='gmessage-detail'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='gmessage-delete'),
    url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='gmessage-undelete'),
    url(r'^trash/$', trash, name='gmessage-trash'),
)
