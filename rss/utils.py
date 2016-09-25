# coding: utf-8

from __future__ import unicode_literals
import os
import time
import datetime
import feedparser
from django.utils import timezone
from django.conf import settings

from .models import Rss, RssItem
from tools.type_tool import has_list_key, has_str_key, has_dict_key
from tools.template_tool import render_django_template


OUTPUT_DIR = settings.OUTPUT_DIR
KINDLEGEN_BIN_PATH = settings.KINDLEGEN_BIN_PATH


def render_and_write(template_name, context, output_name):
    content = render_django_template(template_name, context=context)
    with open(os.path.join(OUTPUT_DIR, output_name), 'w') as f:
        f.write(content.encode('utf-8'))


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


def build_mobi(rsses):

    data = []
    feed_number = 1
    play_order = 1
    for feed in rsses:
        feed_number += 1
        play_order += 1

        local = {
            'number': feed_number,
            'play_order': play_order,
            'entries': [],
            'title': feed.name,
        }

        entry_number = 0

        for entry in feed.rssitem_set.all():
            play_order += 1
            entry_number += 1

            local_entry = {
                'number': entry_number,
                'play_order': play_order,
                'title': entry.name,
                'description': entry.content,
            }

            local['entries'].append(local_entry)

        data.append(local)

    wrap = {
        'date': datetime.date.today().isoformat(),
        'feeds': data,
    }

    # Render and output templates
    render_and_write('mobi/toc.xml', wrap, 'toc.ncx')
    render_and_write('mobi/toc.html', wrap, 'toc.html')
    render_and_write('mobi/opf.xml', wrap, 'daily.opf')
    for feed in data:
        render_and_write('mobi/feed.html', feed, '%s.html' % feed['number'])
    os.system('{} {}'.format(KINDLEGEN_BIN_PATH, os.path.join(OUTPUT_DIR, 'daily.opf')))
