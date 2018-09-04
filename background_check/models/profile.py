from elasticsearch_dsl import Document, field, InnerDoc, Q
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from nucling.snippet import string
from io import BytesIO


__all__ = [ 'Sub_profile', 'Profile' ]


class Ssn_issued( InnerDoc ):
    state = field.Keyword()
    year = field.Integer()
    date = field.Date()


class Ssn_trace( InnerDoc ):
    is_valid = field.Boolean()
    is_deceased = field.Boolean()

    ssn = field.Keyword()
    human_message = field.Text()
    issued = field.Object( Ssn_issued )


class Inner_sub_profile( InnerDoc ):
    sub_profile_id = field.Keyword()
    status = field.Keyword()

    @property
    def sub_profile( self ):
        return Sub_profile.get( self.sub_profile_id )


class Profile( Document ):
    created_at = field.Date()
    ssn_trace = field.Nested( Ssn_trace )

    meta_sub_profiles = field.Nested( Inner_sub_profile )

    class Index:
        name = "profile"

    @property
    def pk( self ):
        return self.meta.id

    @property
    def sub_profiles( self ):
        return [ p.sub_profile for p in self.meta_sub_profiles ]

    def validate_sub_profiles( self, *sub_profiles_ids ):
        valid_sub_profiles_ids = {
            s.sub_profile_id for s in self.meta_sub_profiles }
        for sub_profile_id in sub_profiles_ids:
            if sub_profile_id not in valid_sub_profiles_ids:
                raise ValueError(
                    "the profile: '{}' dont have the sub profile: '{}'"
                    .format( self.meta.id, sub_profile_id ) )

    def attach_sub_profiles( self, sub_profiles ):
        if not isinstance( self.meta_sub_profiles, list ):
            self.meta_sub_profiles = []
        for sub_profile in sub_profiles:
            self.meta_sub_profiles.append( {
                'sub_profile_id': sub_profile.meta.id,
                'status': 'unknown' } )


class Reason_profile( Document ):
    pass


class Sub_profile( Document ):
    response_str = field.Keyword()
    raw_response_str = field.Keyword()

    source = field.Keyword()
    created_at = field.Date()

    task_id = field.Keyword()

    class Index:
        name = "sub_profile"

    def __init__( self, *args, **kw ):
        raw_response = kw.pop( 'raw_response', None )
        response = kw.pop( 'response', None )
        super().__init__( *args, **kw )
        self.raw_response = raw_response
        self.response = response

    @property
    def response( self ):
        return self._decode_obj( self.response_str )

    @response.setter
    def response( self, value ):
        self.response_str = self._encode_obj( value )

    @property
    def raw_response( self ):
        return self._decode_obj( self.raw_response_str )

    @raw_response.setter
    def raw_response( self, value ):
        self.raw_response_str = self._encode_obj( value )

    def save( self, *args, **kw ):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        super().save( *args, **kw )

    def update_response( self, *args, **kw ):
        kw[ 'raw_response_str' ] = self.raw_response_str
        kw[ 'response_str' ] = self.response_str
        return self.update( *args, **kw )

    @classmethod
    def _encode_obj( cls, obj ):
        if isinstance( obj, ( list, dict ) ):
            return string.decode( JSONRenderer().render( obj ) )
        elif obj is None:
            return None
        else:
            raise NotImplementedError(
                "only can encode lists and dicts, received "
                "type: {}, repr: {}".format(
                    type( obj ), repr( obj ) ) )

    @classmethod
    def _decode_obj( cls, obj_str ):
        try:
            if obj_str is None:
                return None
            if isinstance( obj_str, str ):
                obj_str = BytesIO( obj_str.encode( 'utf-8' ) )
            result = JSONParser().parse( obj_str )
            return result
        except Exception as e:
            raise NotImplementedError(
                "only can decode json strings, received "
                "type: {}, repr: {}".format(
                    type( obj_str), repr( obj_str ) ) ) from e

    class Q:
        @classmethod
        def source_from( cls, source ):
            return Q( 'term', source=source )
