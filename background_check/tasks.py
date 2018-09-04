from celery.utils.log import get_task_logger
from turn_profile.app_celery import turn_profile_task as celery_task
from turn_django.tasks import Task_base
from background_check.models import Sub_profile, Profile
from nucling import donkey
import time


logger = get_task_logger(
    'celery.task.background_check' )

@celery_task.task( bind=True, base=Task_base, ignore_result=True )
def merge_profile( self, subprofile_ids, profile_id ):
    profile = Profile.get( profile_id )
    profile.validate_sub_profiles( *subprofile_ids )
    sub_profiles = profile.sub_profiles
    responses = [ s.response for s in sub_profiles ]
    responses_compresses = [ donkey.compress( r ) for r in responses ]
    if len( subprofile_ids ) > 1:
        keys = [ set( r.keys() ) for r in responses_compresses ]
        intersection_keys = set.intersection( *keys )
        if intersection_keys:
            raise ValueError( "cannot merge the keys" )

    for response in responses_compresses:
        for k, v in response.items():
            donkey.setter( k, profile, v )

    profile.save()
