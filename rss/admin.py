from django.contrib import admin

from rss.models import Rss, RssItem, RssCategory


@admin.register(Rss)
class RssAdmin(admin.ModelAdmin):
    pass


@admin.register(RssItem)
class RssItemAdmin(admin.ModelAdmin):
    pass


@admin.register(RssCategory)
class RssCategoryAdmin(admin.ModelAdmin):
    pass
