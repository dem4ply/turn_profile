from rest_framework import serializers
import datetime


class Us_one_validate_issued( serializers.Serializer ):
    date = serializers.SerializerMethodField( source='*' )
    state = serializers.CharField( source='state_issued' )
    year = serializers.IntegerField( source='year_issued' )

    def get_date( self, obj ):
        year = self.fields[ 'year' ].get_attribute( obj )
        if year is None:
            return None
        return datetime.datetime( int( year ), 1, 1 )


class Us_one_validate_ssn_trace( serializers.Serializer ):
    is_deceased= serializers.BooleanField()
    is_random = serializers.SerializerMethodField( source='*' )
    is_valid= serializers.BooleanField()

    human_message = serializers.CharField( source='text_response', required=False )
    issued = Us_one_validate_issued( source='*' )
    ssn= serializers.CharField( source='order.ssn' )

    def get_is_random( self, obj ):
        return False

class Sub_profile( serializers.Serializer ):
    ssn_trace = Us_one_validate_ssn_trace( source='*' )


class Us_one_validate( serializers.Serializer ):
    ssn = serializers.CharField( max_length=9, min_length=9 )
