from __future__ import absolute_import
import os

from celery import Celery
from kombu import Queue
from django.apps import apps


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abantether.settings")
app = Celery("abantether")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


CELERY_TASK_QUEUES = (
    Queue("buy_from_exchange", durable=True, declare=True),
)

