from django.test import TestCase, override_settings
from turn_django.views import page_not_found, server_error
from turn_users.models import Token
from turn_users.tests import get_user_test, get_superuser_test
from rest_framework import status
from rest_framework.test import APIClient
from test_runners.snippet.response import assert_status_code, assert_data
from unittest.mock import Mock


class Test_view_global_404( TestCase ):

    def test_status_code( self ):
        """
        El status code de la respuesta de deberia de ser 404
        """
        request = Mock()
        response = page_not_found( request )
        assert_status_code( response, status.HTTP_404_NOT_FOUND )

    def test_message( self ):
        """
        la respuesta deberia de decir que el recurso no exite
        """
        request = Mock()
        response = page_not_found( request )
        expected = {
            'detail': "The resource does not exist."
        }
        assert_data( response, expected )


class Test_view_global_500( TestCase ):

    def test_status_code( self ):
        """
        El status code de la respuesta de deberia de ser 404
        """
        request = Mock()
        response = server_error( request )
        assert_status_code( response, status.HTTP_500_INTERNAL_SERVER_ERROR )

    def test_message( self ):
        """
        la respuesta deberia de decir que el recurso no exite
        """
        request = Mock()
        response = server_error( request )
        expected = {
            'detail': "Unhandled error."
        }
        assert_data( response, expected )
