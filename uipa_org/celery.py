from __future__ import absolute_import

import os

# This should have been added to supervisord
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uipa_org.settings')
#os.environ.setdefault("DJANGO_CONFIGURATION", "Beta")

from configurations import importer
importer.install(check_options=True)

from celery import Celery
from django.conf import settings


app = Celery('froide')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, related_name='tasks')
