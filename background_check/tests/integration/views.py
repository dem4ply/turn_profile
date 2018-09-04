import unittest
from unittest.mock import patch
from django.test import TestCase, override_settings
from rest_framework import status

from turn_users.tests import get_user_test
from test_runners import authorized as authorized_tests
from test_runners.snippet.response import assert_status_code, get_location
from background_check.factories import (
    Background_check as Background_check_factory,
    Package as Package_factory,
    BGC__us_one_validate as BGC__us_one_validate_factory,
    BGC__us_one_trace as BGC__us_one_trace_factory,
)
from partners.factories import Partner as Partner_factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from vcr_unittest import VCRTestCase


@override_settings( ROOT_URLCONF='background_check.urls' )
class Test_packages_views( APITestCase ):
    url_name = 'packages-list'

    def setUp( self ):
        super().setUp()
        self.user, self.token = get_user_test()
        self.background_checks = Background_check_factory.create_batch(
            size=3 )
        self.partner = Partner_factory.create( user=self.user )
        self.packages = Package_factory.create_batch(
            partner=self.partner, size=3 )
        self.packages[0].background_checks.add( *self.background_checks )
        self.client.credentials( HTTP_AUTHORIZATION=str( self.token ) )

    def test_only_can_get_his_own_package( self ):
        packages = Package_factory.create_batch( size=5 )
        url = reverse( self.url_name )
        response = self.client.get( url )
        packages_ids_other_partner = { a.pk for a in packages }
        packages_ids = {
            a.pk for a in self.user.partner.get().check_packages.all() }
        self.assertNotEqual( packages_ids, packages_ids_other_partner )
        response_ids = { a[ 'pk' ] for a in response.data }
        self.assertSetEqual( response_ids, packages_ids )


@override_settings( ROOT_URLCONF='background_check.urls' )
class Test_users_authorized_list( authorized_tests.Test_list ):
    url_name = 'packages-list'

    def setUp( self ):
        super().setUp()
        self.background_checks = Background_check_factory.create_batch(
            size=3 )
        self.user, self.token = get_user_test()
        self.background_checks = Background_check_factory.create_batch(
            size=3 )
        self.partner = Partner_factory.create( user=self.user )
        self.packages = Package_factory.create_batch(
            partner=self.partner, size=3 )
        self.packages[0].background_checks.add( *self.background_checks )

    def get_url_kw( self ):
        return None

    def get_token( self ):
        user, token = get_user_test()
        return token


class Test_check( APITestCase, VCRTestCase ):
    url_name = 'background_checks:check-list'

    def setUp( self ):
        super().setUp()
        self.user, self.token = get_user_test()
        self.background_check = BGC__us_one_validate_factory.create()
        self.partner = Partner_factory.create( user=self.user )
        self.package = Package_factory.create( partner=self.partner )

        self.package.background_checks.add( self.background_check )
        self.client.credentials( HTTP_AUTHORIZATION=str( self.token ) )

    def test_validate_should_the_error( self ):
        url = reverse(
            self.url_name, kwargs={ 'package_pk': self.package.pk } )
        response = self.client.post( url, data={ 'ssn': '1' } )
        assert_status_code( response, status.HTTP_400_BAD_REQUEST )
        self.assertIn( self.background_check.name, response.data )
        validate_errors = response.data[ self.background_check.name ]
        self.assertIn( 'ssn', validate_errors )
        self.assertEqual( validate_errors[ 'ssn' ][0].code, 'min_length' )

    def test_should_return_the_url_to_get_the_profile( self ):
        url = reverse(
            self.url_name, kwargs={ 'package_pk': self.package.pk } )
        response = self.client.post(
            url, data={ 'ssn': '123456789', '_use_factory': 'default' } )
        assert_status_code( response, status.HTTP_201_CREATED )

        response_profile = get_location( response, client=self.client )
        assert_status_code( response_profile, status.HTTP_200_OK )


class Test_check_two_background_checks( APITestCase, VCRTestCase ):
    url_name = 'background_checks:check-list'

    def setUp( self ):
        super().setUp()
        self.user, self.token = get_user_test()
        self.background_check_validate = BGC__us_one_validate_factory.create()
        self.background_check_trace = BGC__us_one_trace_factory.create()
        self.partner = Partner_factory.create( user=self.user )
        self.package = Package_factory.create( partner=self.partner )

        self.package.background_checks.add( self.background_check_validate )
        self.package.background_checks.add( self.background_check_trace )
        self.client.credentials( HTTP_AUTHORIZATION=str( self.token ) )

    def test_validate_should_the_error( self ):
        url = reverse(
            self.url_name, kwargs={ 'package_pk': self.package.pk } )
        response = self.client.post( url, data={ 'ssn': '1' } )
        assert_status_code( response, status.HTTP_400_BAD_REQUEST )
        self.assertIn( self.background_check_validate.name, response.data )
        validate_errors = response.data[ self.background_check_validate.name ]

        self.assertIn( 'ssn', validate_errors )
        self.assertEqual( validate_errors[ 'ssn' ][0].code, 'min_length' )

        self.assertIn( self.background_check_trace.name, response.data )
        validate_errors = response.data[ self.background_check_trace.name ]

        self.assertIn( 'ssn', validate_errors )
        self.assertEqual( validate_errors[ 'first_name' ][0].code, 'required' )
        self.assertEqual( validate_errors[ 'last_name' ][0].code, 'required' )

    def test_should_return_the_url_to_get_the_profile( self ):
        url = reverse(
            self.url_name, kwargs={ 'package_pk': self.package.pk } )
        response = self.client.post(
            url, data={
                'ssn': '123456789', 'last_name': 'joe', 'first_name': 'jonh',
                '_use_factory': 'default' } )
        assert_status_code( response, status.HTTP_201_CREATED )

        response_profile = get_location( response, client=self.client )
        assert_status_code( response_profile, status.HTTP_200_OK )
