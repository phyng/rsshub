# coding: utf-8

from __future__ import unicode_literals
from django.test import TestCase
from rss.utils import update_rss
from rss.models import Rss, RssItem


class TestRssModel(TestCase):

    def setUp(self):
        pass

    def test_update_rss(self):
        rss = Rss.objects.create(type='rss', name='ifanr', url='http://www.ifanr.com/feed')
        update_rss(rss)
        count = RssItem.objects.filter(rss=rss).count()
        self.assertTrue(count)
        entry = RssItem.objects.filter(rss=rss).first()
        self.assertTrue(entry.name)
        update_rss(rss)
        self.assertTrue(count == RssItem.objects.filter(rss=rss).count())
