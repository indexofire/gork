# -*- coding: utf-8 -*-
from know.core.plugins import registry
from know.core.plugins.base import BasePlugin


class NotifyPlugin(BasePlugin):

    settings_form = 'know.plugins.notifications.forms.SubscriptionForm'

    def __init__(self):
        pass

registry.register(NotifyPlugin)
