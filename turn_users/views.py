from .models import User as User_model, Token as Token_model
from .serializers import User as User_serializer, Token as Token_serializer
from rest_framework.decorators import detail_route

from rest_framework.permissions import IsAdminUser

from rest_framework.response import Response
from turn_django import view_set


class User( view_set.Model_viewset ):
    permission_classes     = [ IsAdminUser ]
    queryset               = User_model.objects.all()
    serializer_class       = User_serializer

    @detail_route( methods=[ 'POST' ] )
    def refresh_token( self, request, pk, format=None ):
        user = self.get_object()
        token = user.refresh_token()
        serializer = Token_serializer( token )
        return Response( serializer.data )


class Token( view_set.Read_only_model_viewset ):
    permission_classes     = [ IsAdminUser ]
    queryset               = Token_model.objects.all()
    serializer_class       = Token_serializer
