# coding: utf-8

from django.core.management.base import BaseCommand
from rss.models import Rss
from rss.utils import update_rss


class Command(BaseCommand):
    help = 'Update rss'

    def handle(self, *args, **options):
        for rss in Rss.objects.all():
            update_rss(rss)
