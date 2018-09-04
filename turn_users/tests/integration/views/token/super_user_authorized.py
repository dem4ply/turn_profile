from django.test import override_settings
from rest_framework import status

from turn_users.tests import get_superuser_test
from turn_users.factories import User as User_factory
from test_runners import authorized as authorized_tests


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_tokens_authorized_list( authorized_tests.Test_list ):
    url_name = 'tokens-list'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_token( self ):
        user, token = get_superuser_test()
        return token

    def get_url_kw( self ):
        return { 'users_pk': self.user.pk }


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_tokens_authorized_detail( authorized_tests.Test_retrieve ):
    url_name = 'tokens-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'users_pk': self.user.pk, 'pk': self.user.token.pk }

    def get_token( self ):
        user, token = get_superuser_test()
        return token
