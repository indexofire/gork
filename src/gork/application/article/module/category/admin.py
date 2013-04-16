# -*- coding: utf-8 -*-
from django.contrib import admin
from article.module.category.models import Category, CategoryAdmin


admin.site.register(Category, CategoryAdmin)
