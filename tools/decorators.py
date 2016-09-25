# coding: utf-8

from __future__ import unicode_literals


def add_attr(**attrs):

    def _decorator(func):

        def _wrap(*args, **kwargs):
            return func(*args, **kwargs)

        for k, v in attrs.items():
            setattr(_wrap, k, v)

        return _wrap

    return _decorator
