#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Ryan Kanno <ryankanno@localkinegrinds.com>
#
# Distributed under terms of the MIT license.

from uipa_org.celery import app as celery_app


@celery_app.task
def test(*args, **kwargs):
    logger = test.get_logger()
    logger.info("TESTING")
