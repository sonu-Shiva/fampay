from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('config', backend='amqp', broker='amqp://')
app = Celery(
    'config',
    backend=settings.CELERY_RESULT_BACKEND,
    broker=settings.CELERY_BROKER_URL,
    include=[
        'apps.celery.tasks',
    ]
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
