# coding: utf-8

from django.core.management.base import BaseCommand
from account.models import User
from rss.utils import send_user_file


class Command(BaseCommand):
    help = 'send user file'

    def handle(self, *args, **options):
        for user in User.objects.all():
            send_user_file(user)
