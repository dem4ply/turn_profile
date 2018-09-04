from django.test import TestCase, override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from turn_users.models import Token, User
from turn_users.tests import get_user_test, get_superuser_test
from turn_users.factories import User as User_factory
from test_runners import unauthorized as unauthorized_tests


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_unauthorized_list( unauthorized_tests.Test_list ):
    url_name = 'users-list'

    def setUp( self ):
        super().setUp()
        User_factory.create()

    def get_url_kw( self ):
        return None


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_unauthorized_detail( unauthorized_tests.Test_retrieve ):
    url_name = 'users-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_unauthorized_create( unauthorized_tests.Test_create ):
    url_name = 'users-detail'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_post_data( self ):
        return None


@override_settings( ROOT_URLCONF='turn_users.urls' )
class Test_users_unauthorized_refresh_token( unauthorized_tests.Test_create ):
    url_name = 'users-refresh-token'

    def setUp( self ):
        super().setUp()
        self.user = User_factory.create()

    def get_url_kw( self ):
        return { 'pk': self.user.pk }

    def get_post_data( self ):
        return None
