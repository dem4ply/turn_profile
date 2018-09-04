from turn_profile.app_celery import turn_profile_task as celery_task
from celery.utils.log import get_task_logger

logger = get_task_logger( 'celery.task.base' )


class Task_base( celery_task.Task ):
    abstract = True

    def on_success( self, retval, task_id, args, kwargs ):
        extra = {
            'task_id': task_id, 'task_success': 1
        }
        logger.info( "sucess task %s" % task_id, extra=extra )
        super().on_success( retval, task_id, args, kwargs )

    def on_retry( self, exc, task_id, args, kwargs, einfo ):
        extra = {
            'task_id': task_id, 'task_retry': 1
        }
        logger.error( "retry task %s" % task_id, exc_info=exc, extra=extra )
        super().on_retry( exc, task_id, args, kwargs, einfo )

    def on_failure( self, exc, task_id, args, kwargs, einfo ):
        extra = {
            'task_id': task_id, 'task_fail': 1
        }

        logger.error( "fail task %s" % task_id, exc_info=exc,
                      extra=extra )
        super().on_failure( task_id, exc, args, kwargs, einfo )
