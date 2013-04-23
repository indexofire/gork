# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from article.models import Article
from article.module.category.models import Category

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
        if hasattr(self.request, '_feincms_extra_context') and 'app_config' in self.request._feincms_extra_context:
            return (self.get_template_names(), context)
        return super(AppContentMixin, self).render_to_response(context, **response_kwargs)


class ArticleDetail(AppContentMixin, DetailView):
    """Detail view of article"""
    model = Article

    def get_queryset(self):
        return Article.objects.active()

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleList(AppContentMixin, ListView):
    """List view of articles"""
    model = Article

    def get_queryset(self):
        return Article.objects.active()


from article import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def article_index(request):
    objects = Article.objects.all()
    paginator = Paginator(objects, settings.ARTICLE_PER_PAGE)
    page = request.GET.get('page')
    categories = Category.objects.all()

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return ('article/article_list.html', {
        'articles': articles,
        'categories': categories,
    })
