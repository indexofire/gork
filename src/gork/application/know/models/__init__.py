# -*- coding: utf-8 -*-
from django.core import urlresolvers
from know.models.article import *
from know.models.urlpath import *
from know.core.plugins.loader import load_wiki_plugins


load_wiki_plugins()
original_django_reverse = urlresolvers.reverse
#from feincms.content.application.models import app_reverse
#original_django_reverse = app_reverse

def reverse(*args, **kwargs):
    """
    Now this is a crazy and silly hack, but it is basically here to
    enforce that an empty path always takes precedence over an article_id
    such that the root article doesn't get resolved to /ID/ but /.

    Another crazy hack that this supports is transforming every wiki url
    by a function. If _transform_url is set on this function, it will
    return the result of calling reverse._transform_url(reversed_url)
    for every url in the wiki namespace.
    """
    if isinstance(args[0], basestring) and args[0].startswith('know:'):
        url_kwargs = kwargs.get('kwargs', {})
        path = url_kwargs.get('path', False)
        # If a path is supplied then discard the article_id
        if path is not False:
            url_kwargs.pop('article_id', None)
            url_kwargs['path'] = path
            kwargs['kwargs'] = url_kwargs

        url = original_django_reverse(*args, **kwargs)
        if hasattr(reverse, '_transform_url'):
            url = reverse._transform_url(url)
    else:
        url = original_django_reverse(*args, **kwargs)

    return url

# Now we redefine reverse method
urlresolvers.reverse = reverse
