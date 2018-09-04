from django.contrib.auth.models import BaseUserManager
from django.db import models
from nucling.snippet import madness
from turn_django.managers import Base_64_pk
from nucling.snippet.madness import generate_token


class User_manager( Base_64_pk, BaseUserManager ):

    def create( self, *args, **kw ):
        user = super().create( *args, **kw )
        user.refresh_token()
        return user

    def create_user( self, *args, **kw  ):
        user = self.create( *args, **kw )
        return user

    def create_superuser( self, *args, **kw ):
        if not kw.get( 'password' ):
            kw[ 'password' ] = generate_token()
        user = self.create( *args, is_staff=True, is_superuser=True, **kw )
        return user

    def create_staff_user( self, *args, **kw ):
        user = self.create( *args, is_staff=True, is_superuser=False, **kw )
        return user

    def create_user_test( self, *args, username=None, password=None, **kw ):
        if not username:
            username = madness.generate_string()
        if not password:
            password = 'password'
        user = self.create_user(
            *args, username=username, password=password, **kw )
        return user

    def create_superuser_test(
            self, *args, username=None, password=None, **kw ):
        if not username:
            username = madness.generate_string()
        if not password:
            password = 'password'
        user = self.create_superuser(
            *args, username=username, password=password, **kw )
        return user

    def create_staff_user_test(
            self, *args, username=None, password=None, **kw ):
        if not username:
            username = madness.generate_string()
        if not password:
            password = 'password'
        user = self.create_staff_user(
            *args, username=username, password=password, **kw )
        return user


class Token_manager( models.Manager ):
    def create( self, *args, **kw ):
        if not 'key' in kw:
            kw[ 'key' ] = generate_token( 20 )
        return super().create( *args, **kw )
