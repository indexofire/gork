# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.utils.translation import ugettext as _
from know.core.plugins import registry
from know.core.plugins.base import BasePlugin


class HelpPlugin(BasePlugin):
    """
    """
    slug = 'help'
    urlpatterns = patterns('',)

    sidebar = {'headline': _('Help'),
               'icon_class': 'icon-question-sign',
               'template': 'know/plugins/help/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    markdown_extensions = []

    def __init__(self):
        pass

registry.register(HelpPlugin)
