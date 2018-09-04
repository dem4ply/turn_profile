import unittest
from django.test import TestCase, override_settings
from rest_framework import status

from turn_users.tests import get_user_test, get_staff_user_test
from test_runners import (
    authorized as authorized_tests,
    unauthorized as unauthorized )
from background_check.factories import (
    Background_check as Background_check_factory,
    Package as Package_factory
)
from partners.factories import Partner as Partner_factory
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class Test_partner_view( APITestCase ):
    url_name = 'partners:partners-list'

    def setUp( self ):
        super().setUp()
        self.user, self.token = get_staff_user_test()
        self.partner = Partner_factory.create_batch( size=10 )
        self.client.credentials( HTTP_AUTHORIZATION=str( self.token ) )

    def test_should_be_a_list( self ):
        url = reverse( self.url_name )
        response = self.client.get( url )
        self.assertIsInstance( response.data, list )
        self.assertTrue( response.data )


class Test_partners_views( unauthorized.Test_list ):
    url_name = 'partners:partners-list'
    expected_status_code = status.HTTP_403_FORBIDDEN

    def setUp( self ):
        super().setUp()
        self.partner = Partner_factory.create_batch( size=10 )

    def get_url_kw( self ):
        return None

    def get_token( self ):
        user, token = get_user_test()
        return token
