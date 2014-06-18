# coding: utf-8

from django import template

from new_django_project._lib.template_layer_registry import Registry


register = template.Library()

@register.simple_tag(takes_context=True)
def registry_set(context, key, value):
    if isinstance(context.get('registry'), Registry):
        context.get('registry').set(key, value)
    return ''

@register.assignment_tag(takes_context=True)
@register.simple_tag(takes_context=True)
def registry_get(context, key):
    if isinstance(context.get('registry'), Registry):
        return context.get('registry').get(key)
