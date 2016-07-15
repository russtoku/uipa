# -*- coding: utf-8 -*-
#
# uipa_extras.py
#
# Copyright © 2016 Russ Tokuyama <russtoku@gmail.com>
#
# Distributed under terms of the MIT license.
#

from django.template import Library, Node
from uipa_org.uipa_constants import WELCOME_DELIMITER, REQUEST_DELIMITER
from uipa_org.uipa_constants import WAIVER_DELIMITER

register = Library()

@register.filter
def prefill(body):
    '''
    Insert string into a textarea field
    '''
    body.field.initial = "%s\n\n\n%s\n\n\n%s\n" % (WELCOME_DELIMITER,
                                                   REQUEST_DELIMITER,
                                                   WAIVER_DELIMITER)
    return body

