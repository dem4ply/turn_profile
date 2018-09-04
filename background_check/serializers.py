from rest_framework import serializers
from .models import (
    Background_check as Background_check_model,
    Package as Package_model,
)


class Background_check( serializers.ModelSerializer ):
    class Meta:
        model = Background_check_model
        fields = [ 'name', ]


class Package( serializers.ModelSerializer ):
    background_checks = Background_check( required=False, many=True )

    class Meta:
        model = Package_model
        fields = [ 'pk', 'name', 'background_checks' ]
        read_only_fields = [ 'pk', 'background_checks' ]


class Profile( serializers.Serializer ):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='pk', view_name='background_checks:profiles-detail' )
