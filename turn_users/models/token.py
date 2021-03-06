from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from nucling.snippet.madness import generate_token

AUTH_USER_MODEL = getattr( settings, 'AUTH_USER_MODEL', 'turn_users.User' )

@python_2_unicode_compatible
class Token( models.Model ):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token', )
    key = models.CharField( primary_key=True, max_length=64 )
    create_at = models.DateTimeField( auto_now_add=True )

    def save( self, *args, **kwargs ):
        if not self.key:
            self.key = self.generate_key()
        return super().save( *args, **kwargs )

    def __repr__(self):
        return "{cls}( {key} )".format(
            cls=str( self.__class__ ), key=self.key )

    def __str__(self):
        return "Token %s" % self.key

    def generate_key( self, length=20 ):
        return generate_token( length )
