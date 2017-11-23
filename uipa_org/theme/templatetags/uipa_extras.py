# -*- coding: utf-8 -*-
#
# uipa_extras.py
#
# Copyright © 2016 Russ Tokuyama <russtoku@gmail.com>
#
# Distributed under terms of the MIT license.
#

from django.template import Library, Node
from uipa_org.uipa_constants import WAIVER_DELIMITER

register = Library()

@register.filter
def prefill(body):
    '''
    Insert string into a textarea field
    '''
    body.field.initial = "\n\n\n{0}\n".format(WAIVER_DELIMITER)
    return body

@register.simple_tag
def waiver_delimiter():
    '''
    Returns the waiver delimiter to template
    '''
    return WAIVER_DELIMITER
