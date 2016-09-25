# coding: utf-8

from __future__ import unicode_literals
from django.shortcuts import redirect


def home_view(request):
    return redirect('/admin/')
