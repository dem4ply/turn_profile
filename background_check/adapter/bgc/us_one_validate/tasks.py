from celery.utils.log import get_task_logger
from turn_profile.app_celery import turn_profile_task as celery_task
from turn_django.tasks import Task_base
from background_check.models import Sub_profile


logger = get_task_logger(
    'celery.task.background_check.adapter.bgc.us_one_validate' )

@celery_task.task( bind=True, base=Task_base )
def us_one_validate( self, sub_profile_id, ssn, factory=None ):
    sub_profile = Sub_profile.get( sub_profile_id )
    if not sub_profile:
        self.retry( countdown=2 ** self.request.retries )
    if not sub_profile.task_id:
        sub_profile.update( task_id=self.request.id )


    from background_check.adapter.bgc.us_one_validate import Adapter
    factory = Adapter.get_factory( factory )
    adapter = Adapter()
    raw_result = adapter.raw_run( ssn=ssn, _use_factory=factory )
    result = adapter.parse_to_sub_profile( raw_result )
    sub_profile.raw_response = raw_result
    sub_profile.response = result
    sub_profile.update_response()
    return sub_profile.meta.id
