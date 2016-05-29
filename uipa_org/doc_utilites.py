#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import datetime
from docx import Document


def create_uipa_document_request(
    document_path,
    request_date,
    agency_name,
    agency_contact_information,
    requester_name,
    requester_contact_information,
    requester_email_address,
    request_text,
    should_waive_fees=False):

    # TODO: @ryankanno - Make case insensitive regexs at some point
    DELIMITER_REPLACEMENT_MAP = {
        "[Request_Date]": request_date.isoformat(),
        "[Agency_Name]": agency_name,
        "[Agency_Contact_Information]": agency_contact_information,
        "[Requester_Name]": requester_name,
        "[Requester_Contact_Information]": requester_contact_information,
        "[Requester_Email_Address]": requester_email_address,
        "[Request]": request_text
    }

    document = Document(document_path)
    paragraphs = document.paragraphs

    for idx, paragraph in enumerate(paragraphs):
        for k, v in DELIMITER_REPLACEMENT_MAP.iteritems():
            if k in paragraph.text:
                paragraph.text = paragraph.text.replace(k, v)

        if "[CB]" in paragraph.text:
            paragraph.text = paragraph.text.replace(
                "[CB]",
                "[X]" if should_waive_fees else "[ ]")

    return document


if __name__ == "__main__":
    """
    Testing, yo.
    """
    document = create_uipa_document_request(
        './data/Request-Access-form-12.1.15-fillable.docx',
        datetime.datetime.utcnow(),
        "Department of Development",
        "Ryan Kanno",
        "Sara Kanno",
        "sara@kanno.io",
        "sara@kanno.io",
        "Can I get access to code?",
        False)

    document.save(
        './data/{0}-FALSE-Request-Access-form-12.1.15-fillable.docx'.format(
            datetime.datetime.utcnow().isoformat()))

    document = create_uipa_document_request(
        './data/Request-Access-form-12.1.15-fillable.docx',
        datetime.datetime.utcnow(),
        "Department of Development",
        "Ryan Kanno",
        "Sara Kanno",
        "sara@kanno.io",
        "sara@kanno.io",
        "Can I get access to code?",
        True)

    document.save(
        './data/{0}-TRUE-Request-Access-form-12.1.15-fillable.docx'.format(
            datetime.datetime.utcnow().isoformat()))

# vim: fenc=utf-8
# vim: filetype=python
