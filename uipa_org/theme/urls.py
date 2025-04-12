#!/usr/bin/env python
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from django.urls import re_path
from django.contrib.flatpages.views import flatpage
from django.utils.translation import gettext as _

faq_url_part = _('faq')
help_url_part = _('help')

urlpatterns = [
    re_path(r'^{}/{}/$'.format(help_url_part, faq_url_part), flatpage,
       {'url': '/{}/{}/'.format(help_url_part, faq_url_part)}, name='help-faq'),
]

# vim: fenc=utf-8
# vim: filetype=python
