# -*- coding: utf-8 -*-
import re
from django import template
from django.contrib.auth import get_user_model
from gcache.caches import cache_result


register = template.Library()


@cache_result
def cache_users():
    return get_user_model().objects.select_related()[:9]


class GetNewUserList(template.Node):
    """
    Get Newest Users List
    """
    def __init__(self, var_name, limit):
        self.var_name = var_name
        self.limit = limit

    def render(self, context):
        context[self.var_name] = cache_users()
        return ''


@register.tag
def get_user_list(parser, token):
    """
    Get Newest Users List
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]

    m1 = re.search(r'(.*?) as (\w+)', arg)

    if not m1:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    else:
        format_string, var_name = m1.groups()
        return GetNewUserList(var_name, format_string[0])
