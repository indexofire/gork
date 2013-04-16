# -*- coding: utf-8 -*-
from django.contrib import admin
from sphinxdoc.models import SphinxDocProject, SphinxDoc


class SphinxDocProjectAdmin(admin.ModelAdmin):
    """Admin interface for :class:`~sphinxdoc.models.Project`."""
    list_display = ('name', 'path',)
    prepopulated_fields = {'slug': ('name',)}


class SphinxDocAdmin(admin.ModelAdmin):
    """
    Admin interface for :class:`~sphinxdoc.models.Document`.

    Normally, you shouldn’t need this, since you create new documents via
    the management command.

    """
    pass


admin.site.register(SphinxDocProject, SphinxDocProjectAdmin)
admin.site.register(SphinxDoc, SphinxDocAdmin)
