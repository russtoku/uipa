#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils import translation
from froide.models import FoiRequest
from uipa_org.celery import app as celery_app
import timedelta


logger = get_task_logger(__name__)

NOTIFICATION_SENT_BEFORE_NUM_DAYS = 14


@celery_app.task
def detect_private_will_be_made_public(*args, **kwargs):
    translation.activate(settings.LANGUAGE_CODE)
    num_days_after_due_date = settings.FROIDE_CONFIG.get(
        'make_public_num_days_after_due_date', 365)
    num_days_after_due_date = num_days_after_due_date - NOTIFICATION_SENT_BEFORE_NUM_DAYS

    now = timezone.now()
    due_date_everything_should_be_made_private = now - timedelta(num_days_after_due_date)

    for foirequest in FoiRequest.objects.filter(Q(visibility=0) | Q(visibility=1), is_foi=True, due_date=due_date_everything_should_be_made_private):
        send_mail(u'{0}'.format(
                _("%(site_name)s: Reminder that your request is being made public in 7 days") % {
                    "site_name": settings.SITE_NAME
                },
            ),
            render_to_string("foirequest/emails/became_public.txt", {
                "site_name": settings.SITE_NAME,
                "request": foirequest,
            }),
            settings.DEFAULT_FROM_EMAIL,
            [foirequest.user.email]
        )


@celery_app.task
def make_private_public(*args, **kwargs):
    translation.activate(settings.LANGUAGE_CODE)
    num_days_after_due_date = settings.FROIDE_CONFIG.get(
        'make_public_num_days_after_due_date', 365)
    now = timezone.now()
    due_date_everything_should_be_made_private = now - timedelta(num_days_after_due_date)
    for foirequest in FoiRequest.objects.filter(Q(visibility=0) | Q(visibility=1), is_foi=True, due_date__lte=due_date_everything_should_be_made_private):
        foirequest.visibility = 2
        foirequest.save()
