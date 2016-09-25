# coding: utf-8

from __future__ import unicode_literals
import time
import datetime
import feedparser
from .models import Rss, RssItem
from tools.type_tool import has_list_key, has_str_key, has_dict_key
from django.utils import timezone


class RssUpdateError(Exception):
    pass


def get_entry_unique_id(entry):
    if has_str_key(entry, 'id') and entry['id']:
        return entry['id']
    return entry['link']


def get_entry_content(entry):
    if has_list_key(entry, 'content'):
        for content in entry['content']:
            if has_str_key(content, 'value'):
                return content['value']
    if has_str_key(entry, 'description'):
        return entry['description']


def get_entry_published(entry):
    try:
        date = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
        return timezone.make_aware(date)
    except (KeyError, TypeError):
        return None


def update_rss(rss):

    feed = feedparser.parse(rss.url)
    if feed.status != 200:
        raise RssUpdateError()

    ids = (get_entry_unique_id(i) for i in feed.entries)
    exists_ids = RssItem.objects.filter(unique_id__in=ids).values_list('unique_id', flat=True)
    exists_ids = set(exists_ids)
    new_entires = (i for i in feed.entries if get_entry_unique_id(i) not in exists_ids)

    rssitems = []
    for entry in new_entires:
        rssitem = RssItem(
            rss=rss,
            name=entry.title,
            unique_id=get_entry_unique_id(entry),
            url=entry.link,
            content=get_entry_content(entry),
            published=get_entry_published(entry),
        )
        rssitems.append(rssitem)

    if rssitems:
        RssItem.objects.bulk_create(rssitems)

    return rssitems
