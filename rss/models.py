from __future__ import unicode_literals

from django.db import models
from account.models import User

RSS_TYPE_CHOICES = (
    ('wechat', 'Wechat'),
    ('rss', 'RSS'),
)


class RssBase(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class RssCategory(RssBase):

    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('order', 'id')


class Rss(RssBase):

    user = models.ManyToManyField(User, blank=True, through='RssUser')
    type = models.CharField(max_length=32, choices=RSS_TYPE_CHOICES)
    rsscategory = models.ForeignKey(RssCategory, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '<RSS {}:{}>'.format(self.id, self.name)


class RssUser(models.Model):

    rss = models.ForeignKey(Rss, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_rssitem = models.ForeignKey('RssItem', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('rss', 'user'), )


class RssItem(RssBase):

    rss = models.ForeignKey(Rss)
    name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, db_index=True, unique=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-published', '-created')

    def __unicode__(self):
        return '<RssItem {}:{}:{}>'.format(self.rss.name, self.id, self.name)
