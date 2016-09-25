# coding: utf-8

from django.core.management.base import BaseCommand
from rss.models import Rss
from rss.utils import build_mobi


class Command(BaseCommand):
    help = 'build mobi'

    def handle(self, *args, **options):
        build_mobi(Rss.objects.all())
