# coding: utf-8

from django.template import engines, Template, Context


def render_django_template(template_name, context=None):
    if context is None:
        context = {}
    django_engine = engines['django']
    template = django_engine.get_template(template_name)
    content = template.render(Context(context))
    return content
