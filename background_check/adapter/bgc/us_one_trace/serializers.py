from rest_framework import serializers


class Phone( serializers.Serializer ):
    number = serializers.CharField( source='phone_info.phone_number' )
    is_public = serializers.BooleanField( source='phone_info.number_is_public' )


class Address( serializers.Serializer ):
    city = serializers.CharField()
    county = serializers.CharField()
    state = serializers.CharField()
    date_first_seen = serializers.DateField()
    date_last_seen = serializers.DateField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    postal_code = serializers.CharField()
    postal_code_4 = serializers.CharField( source='postal_code4' )
    is_verified = serializers.BooleanField( source='verified' )

    street = serializers.CharField( source='street.name' )
    number = serializers.CharField( source='street.number' )
    post_direction = serializers.CharField( source='street.post_direction' )
    pre_direction = serializers.CharField( source='street.pre_direction' )
    suffix = serializers.CharField( source='street.suffix' )


class Sub_profile( serializers.Serializer ):
    addresses = Address( many=True, source='records' )
    phones = Phone( many=True, source='records' )


class Us_one_trace( serializers.Serializer ):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    ssn = serializers.CharField( max_length=9, min_length=9 )
