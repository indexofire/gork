# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse


def ajax_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        js = json.dumps({'not_authenticated': True})
        return HttpResponse(js, mimetype='application/json', status=401)
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
