from rest_framework import serializers
from nucling.snippet.madness import generate_password
from turn_users.models import Token as Token_model, User as User_model


class Token( serializers.ModelSerializer ):
    class Meta:
        model = Token_model
        fields = [ 'key', 'create_at' ]


class User( serializers.ModelSerializer ):
    token = Token( required=False )

    class Meta:
        model = User_model
        fields = [ 'pk', 'is_active', 'token' ]
        read_only_fields = [ 'is_active', 'token', 'pk' ]

    def create( self, validate_data ):
        user = User_model.objects.create_user(
            username=generate_password(), password=generate_password() )
        return user
