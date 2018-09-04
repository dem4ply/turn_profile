import unittest
from unittest.mock import patch
from background_check.models import Sub_profile as Sub_profile_model
from background_check.factories import Sub_profile as Sub_profile_factories
from datetime import datetime
from vcr_unittest import VCRTestCase
from background_check.factories import (
    Sub_profile as Sub_profile_factory,
    Sub_profile_empty as Sub_profile_empty_factory,
    Background_check as Background_check_factory,
    Package as Package_factory,
    BGC__us_one_validate as BGC__us_one_validate_factory,
    Profile as Profile_factory,
)
from partners.factories import Partner as Partner_factory
from turn_users.tests import get_user_test
from rest_framework.exceptions import ValidationError


class Test_package_model( VCRTestCase ):

    def setUp( self ):
        super().setUp()
        self.user, self.token = get_user_test()
        self.background_check = BGC__us_one_validate_factory.create()
        self.partner = Partner_factory.create( user=self.user )
        self.package = Package_factory.create( partner=self.partner )

        self.package.background_checks.add( self.background_check )

    def test_validate_should_check_with_all_the_background_checks( self ):
        with self.assertRaises( ValidationError ):
            self.package.validate( { 'ssn': '1' } )
        self.package.validate( { 'ssn': '123456789' } )

    def test_validate_should_add_the_key_with_the_name_of_the_bc( self ):
        try:
            self.package.validate( { 'ssn': '1' } )
        except ValidationError as e:
            self.assertIn( self.background_check.name, e.detail )
        else:
            self.fail( "i should raise a exception" )

    def test_build_signatures_should_return_all_subprofiles( self ):
        profile = Profile_factory.build()
        sub_profiles, group = self.package.build_signatures(
            profile, { 'ssn': '123456789' }, _use_factory='default' )
        self.assertIsInstance( sub_profiles, list )
        self.assertTrue( sub_profiles, "no return subprofiles"  )
        for sub_profile in sub_profiles:
            self.assertIsInstance( sub_profile, Sub_profile_model )

    def test_build_signatures_the_group_len_should_eq_sub_profiles( self ):
        profile = Profile_factory.build()
        sub_profiles, group = self.package.build_signatures(
            profile, { 'ssn': '123456789' }, _use_factory='default' )
        self.assertEqual( len( sub_profiles ), len( group.tasks ) )

    def test_build_signatures_all_the_sub_profile_have_ids( self ):
        profile = Profile_factory.build()
        sub_profiles, group = self.package.build_signatures(
            profile, { 'ssn': '123456789' }, _use_factory='default' )
        for sub_profile in sub_profiles:
            self.assertTrue( sub_profile.meta.id )
