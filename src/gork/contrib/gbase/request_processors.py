# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
#from django.contrib.auth.models import AnonymousUser


def authenticated_request_processor(page, request):
    """
    Feincms page request processor.
    Adding it to system will ask for login in all pages.
    """
    #if request.user is not AnonymousUser and request.user.has_perm('page.can_view'):
    #    return
    #else:
    #    return ''
    #if not request.user.is_authenticated():
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('gauth-login'))

    #if request.user.is_active():
    #    return HttpResponseRedirect(reverse('gauth-activate-user'))
