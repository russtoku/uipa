#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from contextlib import contextmanager
from django.conf import settings
from django.core.files import File
from django.dispatch import receiver
from doc_utilities import create_uipa_document_request_from_foi_request
from froide.foirequest.file_utils import convert_to_pdf
from froide.foirequest.models import FoiAttachment
from froide.foirequest.models import FoiRequest
import os
from tempfile import mkstemp


@contextmanager
def temp_filename(suffix='', prefix='tmp', dir=None, delete=True):
    fd, name = mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    try:
        os.close(fd)
        yield name
    finally:
        if delete:
            try:
                os.remove(name)
            except OSError:
                pass


@receiver(FoiRequest.request_created,
          dispatch_uid="create_and_attach_uipa_document_request")
def create_and_attach_uipa_document_request(sender, **kwargs):
    foi_request = sender
    document = create_uipa_document_request_from_foi_request(foi_request)

    with temp_filename() as temp_fn:
        document.save(temp_fn + ".extension_for_convert_to_pdf")

        result_file_path = convert_to_pdf(
            temp_fn,
            binary_name=settings.FROIDE_CONFIG.get(
                'doc_conversion_binary'
            ),
            construct_call=settings.FROIDE_CONFIG.get(
                'doc_conversion_call_func'
            )
        )
        message = foi_request.messages[0]

        if message and result_file_path:
            with open(result_file_path, 'rb') as f:
                filename = "records_request.pdf"
                new_file = File(f)
                foi_att = FoiAttachment(belongs_to=message,
                                        approved=False,
                                        filetype='application/pdf')
                foi_att.file = new_file
                foi_att.size = new_file.size
                foi_att.file.save(filename, new_file)
                foi_att._committed = False
                foi_att.save()

# vim: fenc=utf-8
# vim: filetype=python
