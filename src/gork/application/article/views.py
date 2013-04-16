# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from article.models import Article


class AppContentMixin(object):
    """
    Mixin for content of article

    Usage:
        class AppView(AppContentMixin, SomeGenericView):
            model = AppModel
            def get_queryset(self):
                ...
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Rewrite default render_to_response function. It returns the template
        tuple needed for FeinCMS App Content.
        """
        if hasattr(self.request, '_feincms_extra_context') and \
                'app_config' in self.request._feincms_extra_context:
            return (self.get_template_names(), context)
        return super(AppContentMixin, self).render_to_response(context,
                                                               **response_kwargs)


class ArticleDetail(AppContentMixin, DetailView):
    """Detail view of article"""
    model = Article

    def get_queryset(self):
        return Article.objects.active()


class ArticleList(AppContentMixin, ListView):
    """List view of articles"""
    model = Article

    def get_queryset(self):
        return Article.objects.active()
