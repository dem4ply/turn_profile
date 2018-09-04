from rest_framework import serializers
from .models import Partner as Partner_model


class Partner( serializers.ModelSerializer ):
    class Meta:
        model = Partner_model
        fields = [ 'pk', 'name',  ]
        read_only_fields = [ 'pk' ]
