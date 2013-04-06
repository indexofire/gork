# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.raw.models import RawContent
from gform.content import FormContent
#from gbase.request_processors import authenticated_request_processor


# Register page extensions
Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.changedate',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.symlinks',
    'feincms.module.page.extensions.titles',
    'gbase.extensions.menu_class',
    #'feincms.module.page.extensions.translations',
)

# Loading templates for Page models
Page.register_templates(
    {
        'key': 'index',
        'title': _('Index Page'),
        'path': 'layout_index.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
    {
        'key': '1col',
        'title': _('One Columns Page'),
        'path': 'layout_1col.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
    {
        'key': '2col',
        'title': _('Two Columns Page'),
        'path': 'layout_2col.html',
        'regions': (
            ('main', _('Main content area')),
            ('left', _('Left Side'), 'inherited'),
        ),
    },
    {
        'key': '3col',
        'title': _('Three Columns Page'),
        'path': 'layout_3col.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
            ('right', _('Right Side'), 'inherited'),
        ),
    },
    {
        'key': 'app',
        'title': _('Application Page'),
        'path': 'layout_app.html',
        'regions': (
            ('application', _('Application')),
        ),
    },
)

Page.create_content_type(RichTextContent)
Page.create_content_type(FormContent)
Page.create_content_type(RawContent)
#Page.register_request_processor(authenticated_request_processor)


Page.create_content_type(
    ApplicationContent,
    APPLICATIONS=(
        ('know.urls', 'Knowledge Application'),
        ('ask.urls', 'Ask Application'),
    ),
)
