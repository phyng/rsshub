# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rss', '0002_auto_20161007_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='rss',
            name='user',
            field=models.ManyToManyField(blank=True, through='rss.RssUser', to=settings.AUTH_USER_MODEL),
        ),
    ]