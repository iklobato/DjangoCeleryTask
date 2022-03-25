from __future__ import absolute_import
import os
from celery import Celery
from djangoCeleryTest import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoCeleryTest.settings')
app = Celery('djangoCeleryTest')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
