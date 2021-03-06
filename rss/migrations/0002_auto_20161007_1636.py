# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rss', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RssUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_rssitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rss.RssItem')),
            ],
        ),
        migrations.RemoveField(
            model_name='rss',
            name='user',
        ),
        migrations.AddField(
            model_name='rssuser',
            name='rss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rss.Rss'),
        ),
        migrations.AddField(
            model_name='rssuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
