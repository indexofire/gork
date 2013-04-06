# -*- coding: utf-8 -*-
from django.contrib import admin
#from mptt.admin import MPTTModelAdmin
#from django.utils.translation import ugettext_lazy as _
from feincms.admin import tree_editor  # , item_editor
from ask.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title', 'author')


class PostTreeAdmin(tree_editor.TreeEditor):
    fieldsets = [
        ('Basic Fields', {
            'fields': ['author', 'lastedit_user', 'title', 'content', 'type', 'parent'],
        }),
        ('Time Fields', {
            'fields': ['creation_date', 'lastedit_date'],
        }),
        ('Tags', {
            'fields': ['tags', ],
        }),
    ]
    list_display = ('title', 'type')
    #active_toggle = tree_editor.ajax_editable_boolean('active', _('active'))
    list_filter = ('author', )


admin.site.register(Post, PostTreeAdmin)
