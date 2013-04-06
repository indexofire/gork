# -*- coding: utf-8 -*-
from django.contrib import admin
from gnotify.models import Notification, NotificationType, Settings, Subscription
from gnotify.settings import ENABLE_ADMIN


if ENABLE_ADMIN:
    admin.site.register(NotificationType)
    admin.site.register(Notification)
    admin.site.register(Settings)
    admin.site.register(Subscription)
