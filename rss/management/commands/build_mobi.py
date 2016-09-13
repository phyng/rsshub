# coding: utf-8

from django.core.management.base import BaseCommand
import os
import datetime
from rss.models import Rss, RssItem
from rss.utils import update_rss
from django.conf import settings
from tools.template_tool import render_django_template


OUTPUT_DIR = settings.OUTPUT_DIR
BIN_PATH = os.path.join(settings.BASE_DIR, 'kindlegen')


def render_and_write(template_name, context, output_name):
    content = render_django_template(template_name, context=context)
    with open(os.path.join(OUTPUT_DIR, output_name), 'w') as f:
        f.write(content.encode('utf-8'))


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
    os.system('{} {}'.format(BIN_PATH, os.path.join(OUTPUT_DIR, 'daily.opf')))


class Command(BaseCommand):
    help = 'Update rss'

    def handle(self, *args, **options):
        build_mobi(Rss.objects.all())
