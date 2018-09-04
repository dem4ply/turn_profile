from background_check.factories import (
    Sub_profile as Sub_profile_factory,
    Sub_profile_empty as Sub_profile_empty_factory
)
from background_check.adapter.bgc.us_one_trace.tasks import (
    us_one_trace as us_one_trace_task
)
from vcr_unittest import VCRTestCase


class Test_us_one_trace( VCRTestCase ):
    def test_when_the_sub_profile_dont_have_task_is_should_be_added( self ):
        sub_profile = Sub_profile_factory.build()
        sub_profile.save()
        self.assertIsNone( sub_profile.task_id )
        us_one_trace_task.delay(
            sub_profile_id=sub_profile.meta.id,
            ssn='', first_name='', last_name='', factory='default' )
        sub_profile_after_test = sub_profile.get( sub_profile.meta.id )
        self.assertTrue( sub_profile_after_test.task_id )

    def test_save_the_response( self ):
        sub_profile = Sub_profile_empty_factory.build()
        sub_profile.save()
        self.assertIsNone( sub_profile.response )
        self.assertIsNone( sub_profile.raw_response )
        us_one_trace_task.delay(
            sub_profile_id=sub_profile.meta.id,
            ssn='', first_name='', last_name='', factory='default' )
        sub_profile_after_test = sub_profile.get( sub_profile.meta.id )
        self.assertTrue( sub_profile_after_test.response )
        self.assertTrue( sub_profile_after_test.raw_response )
