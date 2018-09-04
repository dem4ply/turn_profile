from background_check.factories import (
    Sub_profile as Sub_profile_factory,
    Sub_profile_empty as Sub_profile_empty_factory
)
from background_check.adapter.bgc.us_one_validate.tasks import (
    us_one_validate as us_one_validate_task
)


def us_one_validate_sub_profile( sub_profile_id, factory='default' ):
    sub_profile = Sub_profile_empty_factory.build()
    sub_profile.meta.id = sub_profile_id
    sub_profile.save()
    assert sub_profile.response is None
    assert sub_profile.raw_response is None

    us_one_validate_task.delay(
        sub_profile_id=sub_profile.meta.id, ssn='', factory=factory )
    sub_profile_after_test = sub_profile.get( sub_profile.meta.id )

    assert sub_profile_after_test.response
    assert sub_profile_after_test.raw_response

    return sub_profile_after_test
