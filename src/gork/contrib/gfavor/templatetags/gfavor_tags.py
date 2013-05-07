# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
#from django.core.cache import cache
from gfavor.settings import *
from gfavor.models import Favorite
from gfavor.utils import build_message


register = template.Library()


@register.inclusion_tag('gfavor/favor_object.html')
def favor_object(object, user, context):
    return


@register.inclusion_tag('gfavor/fav_items.html')
def fav_item(item, user):
    """"""
    favs = Favorite.objects.favorites_for_object(item).select_related()
    users = [fav.user for fav in favs]
    count = len(users)
    counter = build_message(count)
    faved = False
    message = FAV_ADD
    if user.is_authenticated():
        if Favorite.objects.favorites_for_object(item, user).select_related():
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


@register.filter
def is_favorite(object, user):
    """
    Returns True, if object is already in user`s favorite list
    """
    if not user or not user.is_authenticated():
        return False
    return Favorite.objects.favorites_for_object(object, user).count() > 0


@register.inclusion_tag("gfavor/favorite_add_remove.html", takes_context=True)
def add_remove_favorite(context, object, user):
    favorite = None
    content_type = ContentType.objects.get_for_model(object)
    if user.is_authenticated():
        try:
            favorite = Favorite.objects.favorites_for_object(object, user=user)[0]
        except:
            favorite = None
        #if favorite:
        #    favorite = favorite[0]
        #else:
        #    favorite = None
        print favorite

    return {"object": object,
            "content_type": content_type,
            "user": user,
            "favorite": favorite,
            "request": context['request']}
