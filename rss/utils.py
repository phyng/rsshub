# coding: utf-8

from __future__ import unicode_literals
import os
import uuid
import time
import datetime
from PIL import Image
import requests
import feedparser
from pyquery import PyQuery as pq

from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.lru_cache import lru_cache

from .models import Rss, RssItem, RssUser
from tools.type_tool import has_list_key, has_str_key, has_dict_key
from tools.template_tool import render_django_template


OUTPUT_DIR = settings.OUTPUT_DIR
IMG_DIR = os.path.join(OUTPUT_DIR, 'img')
LOCK_FILE = os.path.join(OUTPUT_DIR, 'LOCK')
KINDLEGEN_BIN_PATH = settings.KINDLEGEN_BIN_PATH
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)


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


@lru_cache(maxsize=None)
def download_img(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
    except Exception:
        return
    filename = str(uuid.uuid4())
    path = os.path.join(IMG_DIR, filename)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        try:
            im = Image.open(path)
            im.thumbnail((500, 500), Image.ANTIALIAS)
            im = im.convert('L')
            im.save(path + '.jpeg', "JPEG")
        except IOError:
            return
        finally:
            os.remove(path)

        return 'img/{}.jpeg'.format(filename)


def update_rss_coent(content):
    if not content:
        return content
    try:
        document = pq(content)
    except ValueError:
        return content

    for img in document('img'):
        src = img.attrib.get('src', '')
        if src:
            try:
                path = download_img(src)
            except Exception:
                continue
            if path:
                img.attrib['src'] = path
                img.attrib['middle'] = 'true'

    return str(document)


def build_mobi(rsses):

    if os.path.exists(LOCK_FILE):
        return

    os.mknod(LOCK_FILE)

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
            'title': feed['rss'].name,
        }

        entry_number = 0

        for entry in feed['rssitems']:
            play_order += 1
            entry_number += 1

            local_entry = {
                'number': entry_number,
                'play_order': play_order,
                'title': entry.name,
                'description': update_rss_coent(entry.content),
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

    os.remove(LOCK_FILE)


def send_file(to, subject, file_path):

    email = EmailMessage(
        subject,
        subject,
        settings.EMAIL_HOST_USER,
        to,
    )

    email.attach_file(file_path)
    email.send()


def build_user_rss(user):

    rssusers = RssUser.objects.filter(user=user)
    if not rssusers.exists():
        return

    rsses = []
    for rssuser in rssusers:
        rssitems = rssuser.rss.rssitem_set.all()
        """
        if rssuser.last_rssitem:
            rssitems = rssitems.filter(id__gt=rssuser.last_rssitem_id)
        """
        yestoday = datetime.date.today() - datetime.timedelta(days=1)
        rssitems = rssitems.filter(
            published__year=yestoday.year,
            published__month=yestoday.month,
            published__day=yestoday.day,
        )
        rssitems = list(rssitems)
        if rssitems:
            rsses.append(dict(rssuser=rssuser, rss=rssuser.rss, rssitems=rssitems))

    if rsses:
        build_mobi(rsses)
        for feed in rsses:
            feed['rssuser'].last_rssitem_id = max([i.id for i in feed['rssitems']])
            feed['rssuser'].save()

        return rsses


def send_user_file(user):
    build_user_rss(user)
    send_file(settings.TEST_EMAILS, 'hello', settings.MOBI_PATH)
