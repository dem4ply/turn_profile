## Broker settings.
BROKER_URL = 'amqp://turn_profile:password@Chino:5672/turn_profile_vhost'

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('myapp.tasks', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_ANNOTATIONS = {
    '*': {
        'rate_limit': '5/s'
    }
}

from kombu import Exchange, Queue

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERY_QUEUES = (
    Queue('default', Exchange('task', 'topic'), routing_key='default'),
    Queue('debug',   Exchange('task_debug', 'topic'), routing_key='*.debug.*'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = "tasks"
CELERY_DEFAULT_EXCHANGE_TYPE = "topic"
CELERY_DEFAULT_ROUTING_KEY = "task.default"

CELERY_ROUTES = {
    'default': {
        'binding_key': 'task.#',
    },
    'turn_profile.task.debug_task': {
        'queue': 'debug',
        'binding_key': 'task.debug.*',
        'exchange': 'task_debug'
    }
}

# from celery.schedules import crontab
# from datetime import timedelta

CELERYBEAT_SCHEDULE = {
}

CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
