from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

__all__ = [ 'turn_profile_task' ]

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'turn_profile.settings' )


turn_profile_task = Celery( 'turn_profile' )

turn_profile_task.config_from_object( 'django.conf:settings' )
turn_profile_task.autodiscover_tasks( [
    'background_check.adapter.bgc.us_one_trace',
    'background_check.adapter.bgc.us_one_validate',
] )
turn_profile_task.autodiscover_tasks()
