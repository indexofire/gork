# -*- coding: utf-8 -*-
import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from gbase.decorators import ajax_login_required
from gfavor.settings import *
from gfavor.models import Favorite
from gfavor.utils import build_message


@ajax_login_required
def ajax_fav(request, ctype_id, obj_id):
    """add ajax favorte"""
    ctype = get_object_or_404(ContentType, pk=ctype_id)
    item = ctype.get_object_for_this_type(pk=obj_id)
    if Favorite.objects.filter(user=request.user, content_type=ctype, object_id=obj_id):
        fav = Favorite.objects.get(user=request.user, content_type=ctype, object_id=obj_id)
        fav.delete()
        count = Favorite.objects.favorites_for_object(item).count()
        data_dict = {'id': 0, 'message': FAV_ADD, 'counter': build_message(count), }
    else:
        fav = Favorite.objects.create_favorite(item, request.user)
        count = Favorite.objects.favorites_for_object(item).count()
        data_dict = {
            'id': fav.id,
            'message': FAV_REMOVE,
            'counter': build_message(count),
        }
    return HttpResponse(json.dumps(data_dict), mimetype='application/javascript')
