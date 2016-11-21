#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

import datetime
from docx import Document
import os
from uipa_org.uipa_constants import (WELCOME_DELIMITER,
                                     WAIVER_DELIMITER,
                                     REQUEST_DELIMITER)


def is_requesting_waiver(text):
    '''
    Return True if requestor enters anything below the delimiter in the Your
    Request field on the Request form.
    '''
    parts = text.split(WAIVER_DELIMITER)
    if len(parts) < 2:
        return False
    return len(parts[1].strip()) > 0

def strip_to(phrase, lines):
    '''Return lines after the line that contains the phrase'''
    if not phrase:
        return lines

    start = 0
    for (i, line) in enumerate(lines):
        if line.find(phrase) > -1:
            start = i + 1

    return lines[start:]

def strip_for_request(text):
    ''' Return the text without any delimiters.'''
    lines = strip_to(REQUEST_DELIMITER, text.split('\r\n'))
    lns = [line for line in lines if line.find(WAIVER_DELIMITER) == -1]
    return '\r\n'.join(lns)

def strip_for_email(text):
    ''' Return the text with only the welcome delimiter.'''
    return '%s\r\n\r\n%s' % (WELCOME_DELIMITER, strip_for_request(text))

def create_uipa_document_request_from_foi_request(foi_request, should_waive_fees):
    curr = os.path.dirname(os.path.realpath(__file__))
    return create_uipa_document_request(
        os.path.join(curr, 'data/Request-Access-form-12.1.15-fillable.docx'),
        datetime.datetime.utcnow(),
        foi_request.public_body.name,
        foi_request.public_body.email,
        foi_request.secret_address,
        foi_request.secret_address,
        foi_request.secret_address,
        foi_request.description,
        should_waive_fees)


def create_uipa_document_request(
    document_path,
    request_date,
    agency_name,
    agency_contact_information,
    requester_name,
    requester_contact_information,
    requester_email_address,
    request_text,
    should_waive_fees):

    # TODO: @ryankanno - Make case insensitive regexs at some point
    DELIMITER_REPLACEMENT_MAP = {
        "[Request_Date]": request_date.strftime('%m-%d-%Y'),
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
    fee_wavier = False
    document = create_uipa_document_request(
        './data/Request-Access-form-12.1.15-fillable.docx',
        datetime.datetime.utcnow(),
        "Department of Development",
        "Ryan Kanno",
        "Sara Kanno",
        "sara@kanno.io",
        "sara@kanno.io",
        "Can I get access to code?",
        fee_wavier)

    document.save(
        './data/{0}-FALSE-Request-Access-form-12.1.15-fillable.docx'.format(
            datetime.datetime.utcnow().isoformat()))

    fee_wavier = True
    body = "Can I get access to code?\r\n\r\n%s\r\nBecause, it's public." % WAIVER_DELIMITER
    stripped_body = strip_for_request(body)

    document = create_uipa_document_request(
        './data/Request-Access-form-12.1.15-fillable.docx',
        datetime.datetime.utcnow(),
        "Department of Development",
        "Ryan Kanno",
        "Sara Kanno",
        "sara@kanno.io",
        "sara@kanno.io",
        stripped_body,
        fee_wavier)

    document.save(
        './data/{0}-TRUE-Request-Access-form-12.1.15-fillable.docx'.format(
            datetime.datetime.utcnow().isoformat()))

# vim: fenc=utf-8
# vim: filetype=python
