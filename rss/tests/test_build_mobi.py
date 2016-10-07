# coding: utf-8

from __future__ import unicode_literals
from django.test import TestCase

from account.models import User
from rss.utils import update_rss, build_user_rss
from rss.models import Rss, RssItem, RssUser


class TestBuildMobi(TestCase):

    def setUp(self):
        pass

    def test_build_mobi(self):
        rss = Rss.objects.create(type='rss', name='ifanr', url='http://www.ifanr.com/feed')
        update_rss(rss)
        count = RssItem.objects.filter(rss=rss).count()
        self.assertTrue(count)

        user = User.objects.create_user(username='test')
        rssuser = RssUser.objects.create(rss=rss, user=user)

        # build
        build_user_rss(user)

        rssuser = RssUser.objects.get(rss=rss, user=user)
        max_rssitem_id = rss.rssitem_set.order_by('-id').first().id
        self.assertTrue(rssuser.last_rssitem_id)
        self.assertTrue(rssuser.last_rssitem_id == max_rssitem_id)
