import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(asctime)s %(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': [ 'console' ],
            'level': os.getenv( 'DJANGO_LOG_LEVEL', 'INFO' ),
        },
        'django': {
            'handlers': [ 'console' ],
            'level': os.getenv( 'DJANGO_LOG_LEVEL', 'INFO' ),
        },
        'django.request': {
            'handlers': [ 'console' ],
            'level': 'ERROR',
            'propagate': True,
        },
        'requests': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'celery.task': {
            'handlers': [ 'console' ],
            'level': os.getenv( 'DJANGO_LOG_LEVEL', 'INFO' ),
            'propagate': True,
        },
    }
}

"""
from celery.signals import setup_logging

@setup_logging.connect
def configure_logging( sender=None, **kwargs ):
    import logging
    import logging.config
    logging.config.dictConfig( LOGGING )
"""
