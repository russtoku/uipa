#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from contextlib import contextmanager
from django.core.files import File
from django.dispatch import receiver
from doc_utilities import create_uipa_document_request_from_foi_request
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
        document.save(temp_fn)
        with open(temp_fn, "r") as f:
            message = foi_request.messages[0]

            if message:
                foi_att = FoiAttachment(belongs_to=message,
                                        name="records_request.doc",
                                        filetype="docx")
                foi_att.file.save("records_request.doc", File(f))
                foi_att.size = foi_att.file.size
                foi_att._committed = False
                foi_att.save()

# vim: fenc=utf-8
# vim: filetype=python
