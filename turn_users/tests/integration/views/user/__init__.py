from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from turn_users.models import Token, User
from turn_users.tests import get_user_test, get_superuser_test
from turn_users.factories import User as User_factory
from test_runners import unauthorized as unauthorized_tests
import unittest


@unittest.skip( 'asdf' )
@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_views( TestCase ):
    model = Token
    path = '/token/'

    def setUp( self ):
        self.client = APIClient( enforce_csrf_checks=True )
        self.super_user, self.super_token  = get_superuser_test()
        self.user, self.user_token = get_user_test()

    def test_fail_with_normal_user( self ):
        response = self.client.get( '/users/',
                                    HTTP_AUTHORIZATION=str( self.user_token ) )

        self.assertEqual( response.status_code, status.HTTP_403_FORBIDDEN )

    def test_access_with_super_user( self ):
        auth = str( self.super_token )
        response = self.client.get( '/users/',
                                    HTTP_AUTHORIZATION=auth )

        self.assertEqual( response.status_code, status.HTTP_200_OK )

    def test_create_user( self ):
        auth = str( self.super_token )
        response = self.client.post(
            '/users/', HTTP_AUTHORIZATION=auth )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            ( "the status code should be 200 instead "
              "of {}\ndata:{}"
              ).format( response.status_code, response.data ) )
        self.assertIsInstance( response.data, dict )
        self.assertIn( 'token', response.data )
        self.assertIn( 'key', response.data[ 'token' ] )
        self.assertIsInstance( response.data[ 'token' ][ 'key' ], str )
        return response.data

    def test_delete_user( self ):
        new_user = self.test_create_user()
        auth = str( self.super_token )
        response = self.client.delete(
            '/users/{}/'.format( new_user[ 'pk' ] ),
            HTTP_AUTHORIZATION=auth )

        self.assertEqual( response.status_code, status.HTTP_204_NO_CONTENT )

    def test_refresh_token( self ):
        data = self.test_create_user()
        auth = str( self.super_token )
        response = self.client.post(
            '/users/{}/refresh_token/'.format( data[ 'pk' ] ),
            HTTP_AUTHORIZATION=auth )

        self.assertEqual( response.status_code, status.HTTP_200_OK )
        self.assertNotEqual(
            data[ 'token' ][ 'key' ], response.data[ 'key' ] )
