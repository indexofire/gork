# -*- coding: utf-8 -*-
from django import template
from know.plugins.macros import settings
from know.plugins.macros.mdx.macro import MacroPreprocessor


register = template.Library()


@register.inclusion_tag(
    'know/plugins/templatetags/article_list.html',
    takes_context=True
)
def article_list(context, urlpath, depth):
    context['parent'] = urlpath
    context['depth'] = depth
    return context


@register.assignment_tag
def allowed_macros():
    for method in settings.METHODS:
        try:
            yield getattr(MacroPreprocessor, method).meta
        except AttributeError:
            continue
