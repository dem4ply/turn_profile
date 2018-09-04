from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .token import Token
from turn_users.managers import User_manager


class User( AbstractBaseUser, PermissionsMixin ):
    """
    """
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$',
        message = "Only alphanumeric characters are allowed." )

    id = models.CharField( _( "User id" ), max_length=64, primary_key=True )
    username = models.CharField( unique=True, max_length=64, )
    is_active = models.BooleanField( default=True, null=False )
    is_staff = models.BooleanField( default=False, null=False )

    objects = User_manager()
    USERNAME_FIELD = 'username'

    def __str__( self ):
        return "pk: {} :: username: {}".format( self.pk, self.username )

    def refresh_token( self ):
        """
        TODO: make test
        refresh the token or make one

        Returns
        -------
        py:class:`turn_user.models.Token`
            new token model
        """
        try:
            if self.token:
                self.token.delete()
        except Token.DoesNotExist:
            pass
        finally:
            return Token.objects.create( user=self )
