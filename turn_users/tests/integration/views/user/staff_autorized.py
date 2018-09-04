from django.test import override_settings
from rest_framework import status

from turn_users.tests import get_staff_user_test
from turn_users.factories import User as User_factory
from test_runners import authorized as authorized_tests


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_list( authorized_tests.Test_list ):
    url_name = 'users-list'

    def setUp( self ):
        super().setUp()
        User_factory.create()

    def get_url_kw( self ):
        return None

    def get_token( self ):
        user, token = get_staff_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_detail( authorized_tests.Test_retrieve ):
    url_name = 'users-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_token( self ):
        user, token = get_staff_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_create( authorized_tests.Test_create ):
    url_name = 'users-list'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return None

    def get_post_data( self ):
        return None

    def get_token( self ):
        user, token = get_staff_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_refresh_token( authorized_tests.Test_create ):
    url_name = 'users-refresh-token'
    expected_status_code = status.HTTP_200_OK

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_post_data( self ):
        return None

    def get_token( self ):
        user, token = get_staff_user_test()
        return token
