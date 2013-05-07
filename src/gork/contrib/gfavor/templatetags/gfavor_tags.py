# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from gfavor.settings import *
from gfavor.models import Favorite
from gfavor.utils import build_message


register = template.Library()


@register.inclusion_tag('gfavor/fav_items.html')
def fav_item(item, user):
    """"""
    favs = Favorite.objects.favorites_for_object(item)
    users = [fav.user for fav in favs]
    count = len(users)
    counter = build_message(count)
    faved = False
    message = FAV_ADD
    if user.is_authenticated():
        if Favorite.objects.favorites_for_object(item, user):
            faved = True
            message = FAV_REMOVE
    ctype = ContentType.objects.get_for_model(item)
    return {
        'faved': faved,
        'message': message,
        'users': users,
        'counter': counter,
        'item': item,
        'ctype': ctype,
    }
