from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from turn_users.models import Token, User
from turn_users.tests import get_user_test, get_superuser_test
from turn_users.factories import User as User_factory
from test_runners import unauthorized as unauthorized_tests


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_tokens_unauthorized_list( unauthorized_tests.Test_list ):
    url_name = 'tokens-list'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'users_pk': self.user.pk }


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_tokens_unauthorized_detail( unauthorized_tests.Test_retrieve ):
    url_name = 'tokens-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'users_pk': self.user.pk, 'pk': self.user.token.pk }
