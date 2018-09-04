from background_check.factories import (
    Sub_profile as Sub_profile_factory,
    Sub_profile_empty as Sub_profile_empty_factory,
    Profile as Profile_factory,
)
from background_check.adapter.bgc.us_one_validate.tasks import (
    us_one_validate as us_one_validate_task
)
from background_check.tasks import merge_profile
from background_check.models import Sub_profile, Profile
from vcr_unittest import VCRTestCase
from background_check.adapter.bgc.us_one_validate import Adapter as BGC_adapter
from background_check.adapter.bgc.us_one_trace import (
    Adapter as BGC_trace_adapter
)


class Test_merge_profile_extra_sub_profiles( VCRTestCase ):

    def set_up_profile( self ):
        self.sub_profile = Sub_profile_factory.build()
        self.sub_profile.meta.id = 'sub_profile_12345'
        self.sub_profile.save()

        self.profile = Profile_factory.build()
        self.profile.attach_sub_profiles( [ self.sub_profile ] )
        self.profile.meta.id = 'sub_profile_12345'
        self.profile.save()

        self.sub_profile_ids = [ self.sub_profile.meta.id ]

    def test_if_send_extra_sub_profiles_should_rasie_valueError( self ):
        self.set_up_profile()
        sub_profiles_ids = [ 'asdf' ] + self.sub_profile_ids
        with self.assertRaises( ValueError ):
            merge_profile( sub_profiles_ids, self.profile.meta.id )


class Test_merge_profile( VCRTestCase ):

    def set_up_profile( self ):
        self.sub_profile = Sub_profile_factory.build()
        self.sub_profile.meta.id = 'sub_profile_12345'
        self.sub_profile.save()

        self.profile = Profile_factory.build()
        self.profile.attach_sub_profiles( [ self.sub_profile ] )
        self.profile.meta.id = 'sub_profile_12345'
        self.profile.save()

        self.sub_profile_ids = [ self.sub_profile.meta.id ]

    def test_should_merge_the_sub_profile( self ):
        self.set_up_profile()
        merge_profile( self.sub_profile_ids, self.profile.meta.id )
        profile = Profile.get( self.profile.meta.id )
        sub_profile = Sub_profile.get( self.sub_profile.meta.id )
        self.assertDictContainsSubset(
            sub_profile.response, profile.to_dict() )


class Test_merge_profile_bgc( VCRTestCase ):

    def setUp( self ):
        super().setUp()
        self.adapter = BGC_adapter()
        self.factory = 'default'

    def set_up_profile( self ):
        self.sub_profile = self.adapter(
            ssn='123456789', _use_factory=self.factory )
        self.sub_profile = Sub_profile.get( self.sub_profile.meta.id )
        del self.sub_profile.meta.version
        self.sub_profile.meta.id = 'bgc_us_one_validate_123456789'
        self.sub_profile.save()

        self.profile = Profile_factory.build()
        self.profile.attach_sub_profiles( [ self.sub_profile ] )
        self.profile.meta.id = 'sub_profile_12345'
        self.profile.save()

        self.sub_profile_ids = [ self.sub_profile.meta.id ]

    def test_should_merge_the_sub_profile( self ):
        self.set_up_profile()
        merge_profile( self.sub_profile_ids, self.profile.meta.id )
        profile = Profile.get( self.profile.meta.id )
        sub_profile = Sub_profile.get( self.sub_profile.meta.id )
        self.assertIn( 'ssn_trace', profile.to_dict() )
        self.assertEqual(
            profile.ssn_trace.ssn,
            sub_profile.response[ 'ssn_trace' ][ 'ssn' ] )

        self.assertEqual(
            profile.ssn_trace.human_message,
            sub_profile.response[ 'ssn_trace' ][ 'human_message' ] )


class Test_merge_profile_bgc_two( VCRTestCase ):

    def setUp( self ):
        super().setUp()
        self.adapter = BGC_adapter()
        self.adapter_trace = BGC_trace_adapter()
        self.factory = 'default'

    def set_up_profile( self ):
        self.sub_profile = self.adapter(
            ssn='123456789', _use_factory=self.factory )
        self.sub_profile = Sub_profile.get( self.sub_profile.meta.id )
        del self.sub_profile.meta.version
        self.sub_profile.meta.id = 'bgc_us_one_validate_123456789'
        self.sub_profile.save()

        self.sub_profile_trace = self.adapter_trace(
            ssn='123456789', first_name='jonh', last_name='doe',
            _use_factory=self.factory )
        self.sub_profile_trace = Sub_profile.get(
            self.sub_profile_trace.meta.id )
        del self.sub_profile_trace.meta.version
        self.sub_profile_trace.meta.id = 'bgc_us_one_trace_123456789'
        self.sub_profile_trace.save()

        self.profile = Profile_factory.build()
        self.profile.attach_sub_profiles(
            [ self.sub_profile, self.sub_profile_trace ] )
        self.profile.meta.id = 'sub_profile_12345'
        self.profile.save()

        self.sub_profile_ids = [
            self.sub_profile.meta.id, self.sub_profile_trace.meta.id ]

    def test_should_merge_the_sub_profile( self ):
        self.set_up_profile()
        merge_profile( self.sub_profile_ids, self.profile.meta.id )
        profile = Profile.get( self.profile.meta.id )
        self.assertIn( 'ssn_trace', profile.to_dict() )
        self.assertIsNotNone( profile.ssn_trace )
        self.assertIsNotNone( profile.addresses )
        self.assertIsNotNone( profile.phones )
