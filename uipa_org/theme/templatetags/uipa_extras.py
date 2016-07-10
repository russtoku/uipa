# -*- coding: utf-8 -*-
#
# uipa_extras.py
#

from django.template import Library, Node

register = Library()

@register.filter
def initial(body, str):
    '''Insert string into a textarea field'''
    body.field.initial = "\n\n\n\n\n%s\n" % str
    return body

