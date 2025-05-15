from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings


__all__ = [ 'chibi_datahouse_task' ]

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'chibi_datahouse.settings' )

chibi_datahouse_task = Celery( 'chibi_datahouse' )

chibi_datahouse_task.config_from_object(
    'django.conf:settings', namespace='CELERY' )
chibi_datahouse_task.autodiscover_tasks( lambda: settings.INSTALLED_APPS )
# print( chibi_datahouse_task._conf )
