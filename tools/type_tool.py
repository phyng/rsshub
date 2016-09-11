# coding: utf-8


def has_dict_key(obj, key):
    return isinstance(obj, dict) and key in obj and isinstance(obj[key], dict)


def has_list_key(obj, key):
    return isinstance(obj, dict) and key in obj and isinstance(obj[key], list)


def has_str_key(obj, key):
    return isinstance(obj, dict) and key in obj and isinstance(obj[key], basestring)


def has_int_key(obj, key):
    return isinstance(obj, dict) and key in obj and isinstance(obj[key], int)
