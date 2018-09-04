from django.test import override_settings

from turn_users.tests import get_user_test
from turn_users.factories import User as User_factory
from test_runners import permission_denail as permission_deanil_test


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_list( permission_deanil_test.Test_list ):
    url_name = 'users-list'

    def setUp( self ):
        super().setUp()
        User_factory.create()

    def get_url_kw( self ):
        return None

    def get_token( self ):
        user, token = get_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_detail( permission_deanil_test.Test_retrieve ):
    url_name = 'users-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_token( self ):
        user, token = get_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_create( permission_deanil_test.Test_create ):
    url_name = 'users-list'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return None

    def get_post_data( self ):
        return None

    def get_token( self ):
        user, token = get_user_test()
        return token


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_authorized_refresh_token( permission_deanil_test.Test_create ):
    url_name = 'users-refresh-token'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_post_data( self ):
        return None

    def get_token( self ):
        user, token = get_user_test()
        return token
