# coding: utf-8

from django import template
from django.conf import settings
from new_django_project.lib import pluralize

register = template.Library()


@register.filter
def hash(h, key, d=None):
    return h.get(key)

@register.filter
def hash_key_isset(h, key):
    return h.has_key(key)


@register.filter
def math_mult(one, two):
    return one * two

import imghdr
@register.filter
def file_is_image(file):
    if imghdr.what(file) in ('jpeg', 'gif', 'png', ):
        return True
    return False

@register.filter
def tag_find_n_remove(l, t):
    l = filter(lambda x: x != t, list(l))
    return l if l else ['all']

@register.filter
def tag_append(l, t):
    l = list(l)
    l.append(t)
    return l


@register.filter
def pluralize_normal(value, arg):
    return pluralize(value, arg)


@register.filter
def replace(string, args):
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]
    return re.sub( search, replace, string )


import re
@register.filter
def date_ru(date, format):
    from pytils.dt import ru_strftime
    if hasattr(settings, format):
        return ru_strftime(format=getattr(settings, format), date=date, inflected=True)
    return ru_strftime(date=date)



class AssignNode(template.Node):
   def __init__(self, name, value):
       self.name = name
       self.value = value

   def render(self, context):
       context[self.name] = self.value.resolve(context, True)
       return ''

@register.tag
def assign(parser, token):
   bits = token.contents.split()
   if len(bits) != 3:
       raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
   value = parser.compile_filter(bits[2])
   return AssignNode(bits[1], value)


@register.assignment_tag
@register.simple_tag()
def settings_attr(key):
    return getattr(settings, key)
