# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from know.core.plugins import registry
from know.core.plugins.base import BasePlugin
from know.plugins.macros import settings
from know.plugins.macros.mdx.macro import MacroExtension
from know.plugins.macros.mdx.toc import WikiTocExtension


class MacroPlugin(BasePlugin):

    slug = settings.SLUG
    sidebar = {'headline': _('Macros'),
               'icon_class': 'icon-play',
               'template': 'know/plugins/macros/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    markdown_extensions = [MacroExtension(), WikiTocExtension()]

    def __init__(self):
        pass

registry.register(MacroPlugin)
