# -*- coding: utf-8 -*-
from gmessage.models import inbox_count_for


def messages_inbox(request):
    if request.user.is_authenticated():
        return {'messages_inbox_count': inbox_count_for(request.user)}
    else:
        return {}
