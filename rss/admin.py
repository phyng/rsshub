# coding: utf-8

from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import messages

from rss.models import Rss, RssItem, RssCategory
from tools.decorators import add_attr
from .utils import update_rss


@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):

    list_display = ['name', 'url', 'created', 'updated']
    actions = ['action_update_rss']

    @add_attr(short_description='Update Rss')
    def action_update_rss(self, request, queryset):
        length = 0
        for rss in queryset:
            rssitems = update_rss(rss)
            length += len(rssitems)
        messages.success(request, 'Add {} rssitem'.format(length))


@admin.register(RssItem)
class RssItemAdmin(admin.ModelAdmin):

    list_display = ['name', 'url', 'published']


@admin.register(RssCategory)
class RssCategoryAdmin(admin.ModelAdmin):
    pass
