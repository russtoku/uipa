#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from django.dispatch import receiver
from froide.foirequest.models import FoiRequest


@receiver(FoiRequest.request_created,
        dispatch_uid="create_and_attach_pdf")
def create_and_attach_pdf(sender, **kwargs):
    print(sender.__dict__)
    print(sender.messages)

# vim: fenc=utf-8
# vim: filetype=python
