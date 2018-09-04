from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import ValidationError
from celery import group
from .profile import Profile
from background_check.tasks import merge_profile
from background_check.managers import (
    Background_check_manager, Package_manager
)


AUTH_USER_MODEL = getattr( settings, 'AUTH_USER_MODEL', 'turn_users.User' )


__all__ = [ 'Background_check', 'Package' ]


class Background_check( models.Model ):
    id = models.CharField(
        _( "Background check id" ), max_length=64, primary_key=True )
    name = models.CharField( max_length=128 )
    adapter = models.CharField( max_length=512 )

    objects = Background_check_manager()

    def get_adapter( self ):
        if self.adapter == 'bgc.us_one_validate':
            from background_check.adapter.bgc.us_one_validate import Adapter
            return Adapter()
        elif self.adapter == 'bgc.us_one_trace':
            from background_check.adapter.bgc.us_one_trace import Adapter
            return Adapter()
        else:
            raise NotImplementedError(
                "the adapter {} no exists".format( self.adapter ) )


class Package( models.Model ):
    id = models.CharField(
        _( "Package id" ), max_length=64, primary_key=True )
    name = models.CharField( max_length=128 )

    background_checks = models.ManyToManyField(
        Background_check, related_name='packages' )
    partner = models.ForeignKey(
        'partners.Partner', on_delete=models.CASCADE,
        related_name='check_packages', )

    objects = Package_manager()

    def validate( self, data ):
        errors = {}
        result = {}
        for bc in self.background_checks.all():
            adapter = bc.get_adapter()
            try:
                result.update( adapter.validate( **data ) )
            except ValidationError as e:
                errors[ bc.name ] = e.detail
        if errors:
            raise ValidationError( errors )
        return result

    def create_profile( self, data ):
        profile = Profile()
        return profile

    def build_signatures( self, profile, data, _use_factory=None ):
        sub_profiles = []
        signatures = []
        for bc in self.background_checks.all():
            adapter = bc.get_adapter()
            valid_data = adapter.validate( **data )
            if _use_factory is None:
                _use_factory = data.get( '_use_factory', None )

            sub_profile, signature = adapter.signature(
                **valid_data, _use_factory=_use_factory )
            sub_profiles.append( sub_profile )
            signatures.append( signature )

        tasks_g = group( *signatures, profile_id=profile.meta.id )
        tasks = tasks_g | merge_profile.signature(
            kwargs={ 'profile_id': profile.meta.id } )

        return sub_profiles, tasks
