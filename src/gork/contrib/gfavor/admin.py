# -*- coding: utf-8 -*-
from django.contrib import admin
from gfavor.models import Favorite


class FavoriteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Favorite, FavoriteAdmin)
