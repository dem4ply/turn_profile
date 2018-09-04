from tetrapod.bgc import bgc as bgc_client
from tetrapod.bgc.factories.us_one_validate import (
    Us_one_trace as Us_one_validate_factory
)
from .serializers import Us_one_validate, Sub_profile as Sub_profile_serializer
from background_check.models import Sub_profile
from .tasks import us_one_validate as us_one_validate_task


class Adapter:
    serializer = Us_one_validate
    source = 'bgc.us_one_validate'

    def run( self, *, ssn, _use_factory=None ):
        sub_profile, signature = self.signature(
            ssn=ssn, _use_factory=_use_factory)
        signature.delay()
        return sub_profile

    def raw_run( self, *, ssn, _use_factory=None ):
        response = bgc_client.us_one_validate(
            _use_factory=_use_factory, ssn=ssn )
        return response

    def signature( self, *, ssn, _use_factory=None ):
        valid_data = self.validate( ssn=ssn )
        if _use_factory is not None and not isinstance( _use_factory, str ):
            raise NotImplementedError
        sub_profile = self.build_sub_profile( None )
        sub_profile.save()
        valid_data[ 'sub_profile_id' ] = sub_profile.meta.id
        valid_data[ 'factory' ] = _use_factory
        task = self.get_tasks()
        signature = task.signature( kwargs=valid_data )
        return sub_profile, signature

    def get_tasks( self ):
        return us_one_validate_task

    def validate( self, *args, raise_exception=True, **kw  ):
        serializer = self.serializer( data=kw )
        serializer.is_valid( raise_exception=raise_exception )
        if serializer.errors:
            return serializer.errors
        return serializer.validated_data

    def build_sub_profile( self, raw_response ):
        parse = Sub_profile_serializer( raw_response, context=raw_response )
        sub_profile = Sub_profile(
            source=self.source, raw_response=raw_response,
            response=parse.data )
        return sub_profile

    def parse_to_sub_profile( self, raw_response ):
        parse = Sub_profile_serializer( raw_response, context=raw_response )
        return parse.data

    @classmethod
    def get_default_factory( cls ):
        return Us_one_validate_factory

    @classmethod
    def get_factory( cls, factory ):
        if factory is None:
            return None
        elif not isinstance( factory, str ):
            raise NotImplementedError
        elif factory == 'default':
            return cls.get_default_factory()
        else:
            raise NotImplementedError

    def __call__( self, *args, **kw ):
        return self.run( *args, **kw )
