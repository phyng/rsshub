from django.contrib import admin

from rss.models import Rss, RssItem, RssCategory


@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):

    list_display = ['name', 'url', 'created', 'updated']


@admin.register(RssItem)
class RssItemAdmin(admin.ModelAdmin):

    list_display = ['name', 'url', 'published']


@admin.register(RssCategory)
class RssCategoryAdmin(admin.ModelAdmin):
    pass
