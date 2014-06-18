# coding: utf-8

from django import template
import math
from django.forms import model_to_dict
from mptt.managers import TreeManager

register = template.Library()

class TreeList(template.Node):
    def __init__(self, name, depth=None, tpl=''):
        self.name = name
        self.depth = int(depth)
        self.tpl = tpl
    def render(self, context):
        if not isinstance(context[self.name], TreeManager):
            raise BaseException("""%s is not instanse of %s""" % (context[self.name], TreeManager))
        return self._render(context[self.name].filter(level=0))
    def _render(self, list, level=0):
        output = []
        for item in list:
            item_output = self.tpl % item.get_advanced_dict() if hasattr(item, 'get_advanced_dict') else model_to_dict(item)
            if item.get_children() and (not self.depth or self.depth-1 > level):
                item_output += self._render(item.get_children(), level+1)
                item_output = ' class="osetr">%s' % item_output
            else:
                item_output = '>%s' % item_output
            output.append(item_output)
        return """<ul class="tree_level_%s"><li%s</li></ul>""" % (level, '</li><li'.join(output))


@register.tag
def mptt_tree_list(parser, token):
    bits = token.split_contents()
    return TreeList(bits[1], bits[2], bits[3].strip(''''"'''))


# only 2 levels :)
class TreeListAsTable(TreeList):
    def _render(self, list, level=0):
        if not level:
            return self._render_zero(list)
        else:
            output = ''
            for i, item in enumerate(list):
                output += self.tpl % item.get_advanced_dict() if hasattr(item, 'get_advanced_dict') else model_to_dict(item)
            return output
    def _render_zero(self, list):
        wrap_when = int(math.ceil(float(len(list)) / 2))
        output = '<table><tr><td class="l">'
        for i, item in enumerate(list):
            if wrap_when == i:
                output += '</td><td class="g"></td><td class="r">'
            output += '<ul class="mb20 mt10">'
            output += '<li class="cat">'
            output += self.tpl % item.get_advanced_dict() if hasattr(item, 'get_advanced_dict') else model_to_dict(item)
            output += '</li>'
            if item.get_descendants():
                output += '<li class="subcat">'
                output += self._render(item.get_descendants(), 1)
                output += '</li>'
            output += '</ul>'
        output += '</td></tr></table>'
        return output


@register.tag
def mptt_tree_list_as_table(parser, token):
    bits = token.split_contents()
    return TreeListAsTable(bits[1], bits[2], bits[3].strip(''''"'''))
