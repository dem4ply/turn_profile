from django.test import TestCase
from unittest.mock import patch
from turn_users.models import User


class Test_user_manager( TestCase ):
    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_user( self, token_save, user_save, ):
        user = User.objects.create_user(
            username='test', password='password' )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )
        self.assertEqual( user.username, "test" )
        self.assertEqual( user.password, "password" )
        self.assertTrue( user.is_active )
        self.assertFalse( user.is_staff )

    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_staff_user( self, user_save, token_save):
        user = User.objects.create_staff_user(
            username='test', password='password' )
        self.assertTrue( user.is_staff )
        self.assertFalse( user.is_superuser )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )

    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_superuser( self, user_save, token_save):
        user = User.objects.create_superuser(
            username='test', password='password' )
        self.assertTrue( user.is_staff )
        self.assertTrue( user.is_superuser )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )

    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_staff_user_test( self, user_save, token_save ):
        user = User.objects.create_staff_user_test()
        self.assertTrue( user.is_staff )
        self.assertFalse( user.is_superuser )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )

    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_superuser_test( self, user_save, token_save ):
        user = User.objects.create_superuser_test()
        self.assertTrue( user.is_staff )
        self.assertTrue( user.is_superuser )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )

    @patch( "turn_users.models.User.save" )
    @patch( "turn_users.models.Token.save" )
    def test_create_user_test( self, user_save, token_save ):
        user = User.objects.create_user_test()
        self.assertFalse( user.is_staff )
        self.assertFalse( user.is_superuser )
        self.assertTrue( user_save.called )
        self.assertTrue( token_save.called )
