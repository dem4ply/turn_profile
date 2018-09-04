import unittest
from background_check.factories import (
    Sub_profile as Sub_profile_factory,
    Sub_profile_with_list as Sub_profile_with_list_factory,
)
from background_check.models import Sub_profile as Sub_profile


class Test_sub_profile_factory( unittest.TestCase ):

    def test_make_a_sub_profile_should_work( self ):
        sub_profile = Sub_profile_factory.build()
        self.assertIsInstance( sub_profile, Sub_profile )

        self.assertIsInstance( sub_profile.response_str, str )
        self.assertIsInstance( sub_profile.raw_response_str, str )

        self.assertIsInstance( sub_profile.response, dict )
        self.assertIsInstance( sub_profile.raw_response, dict )

    def test_make_a_sub_profile_should_work_with_list( self ):
        sub_profile = Sub_profile_with_list_factory.build()
        self.assertIsInstance( sub_profile, Sub_profile )

        self.assertIsInstance( sub_profile.response_str, str )
        self.assertIsInstance( sub_profile.raw_response_str, str )

        self.assertIsInstance( sub_profile.response, list )
        self.assertIsInstance( sub_profile.raw_response, list )
