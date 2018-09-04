from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import Partner_manager
from django.conf import settings


AUTH_USER_MODEL = getattr( settings, 'AUTH_USER_MODEL', 'turn_users.User' )

class Partner( models.Model ):
    """
    Model for the data of each partner organization

    Attributes
    ----------
    id: string
    name: string
    """
    id = models.CharField( _( "Partner id" ), max_length=64, primary_key=True )
    name = models.CharField( max_length=128, )
    users = models.ManyToManyField( AUTH_USER_MODEL, related_name='partner' )

    objects = Partner_manager()
