from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework import status
from rest_framework.response import Response

from turn_users.authentication import Token_simple_authentication
from turn_users.models import User as User_model, Token as Token_model

from rest_framework_nested import routers


factory = APIRequestFactory()


def get_staff_user_test():
    try:
        user = User_model.objects.filter( is_staff=True, is_super=False )[0]
    except:
        user = User_model.objects.create_staff_user_test()
    try:
        token = user.token
    except Token_model.DoesNotExist:
        token = user.refresh_token()
    return user, token

def get_superuser_test():
    try:
        user = User_model.objects.filter( is_staff=True, is_super=True )[0]
    except:
        user = User_model.objects.create_superuser_test()
    try:
        token = user.token
    except Token_model.DoesNotExist:
        token = user.refresh_token()
    return user, token


def get_user_test( pk=None ):
    try:
        user = User_model.objects.filter( is_staff=False )[0]
    except:
        user = User_model.objects.create_user_test( pk=pk )
    try:
        token = user.token
    except Token_model.DoesNotExist:
        token = user.refresh_token()
    return user, token


class Mock_View_authenticated( APIView ):
    permission_classes = ( permissions.IsAuthenticated, )

    def get( self, request ):
        return HttpResponse( {'a': 1, 'b': 2, 'c': 3 } )

    def post( self, request ):
        return HttpResponse( { 'a': 1, 'b': 2, 'c': 3 } )

    def put( self, request ):
        return HttpResponse( { 'a': 1, 'b': 2, 'c': 3 } )


class Mock_view_all_404( viewsets.ViewSet ):
    permission_classes = ( permissions.IsAuthenticated, )

    def list( self, request, format=None ):
        return Response( {}, status=status.HTTP_404_NOT_FOUND )

    def retrieve( self, request, pk, format=None ):
        return Response( {}, status=status.HTTP_404_NOT_FOUND )

    def update( self, request, pk, format=None ):
        return Response( {}, status=status.HTTP_404_NOT_FOUND )


router = routers.SimpleRouter()
router.register( r'fail_soft', Mock_view_all_404, base_name='fail_soft' )

urlpatterns = [
    path(
        r'^token/$',
        Mock_View_authenticated.as_view(
            authentication_classes=[ Token_simple_authentication ] )
    ),
    path( r'', include( ( router.urls, 'turn_users' ), namespace='fail_soft' ), ),
]
