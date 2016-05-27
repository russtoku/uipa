#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.flatpages.views import flatpage
from django.utils.translation import ugettext as _

faq_url_part = _('faq')

urlpatterns = patterns('',
    url(r'^%s/$' % faq_url_part, flatpage,
        {'url': '/%s/' % faq_url_part}, name='faq-index'),
)

# vim: fenc=utf-8
# vim: filetype=python
