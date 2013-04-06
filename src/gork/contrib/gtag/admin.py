# -*- coding: utf-8 -*-
from django.contrib import admin
from gtag.models import Tag, TaggedItem


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Tag, TagAdmin)
