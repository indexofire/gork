# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from article.models import Article
from article.module.category.models import Category


class ArticleList(models.Model):
    number = models.IntegerField()
    if 'article.module.category' in settings.INSTALLED_APPS:
        category = models.ManyToManyField(Category, related_name='cate_name')

    class Meta:
        abstract = True

    def get_queryset_for_render(self):
        return Article.objects.all()

    def render(self, **kwargs):
        objects = Article.objects.all().select_related()[:self.number]
        context = {
            #'object_list': self.get_queryset_for_render()[:self.number],
            'object_list': objects,
            'request': kwargs.get('request'),
        }
        return render_to_string('content/article/article_list.html', context)
