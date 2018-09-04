from .models import Package as Package_model, Profile as Profile_model
from rest_framework.decorators import detail_route

from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework.response import Response
from turn_django import view_set
from .serializers import (
    Package as Package_serializer,
    Profile as Profile_serializer,
)


class Package( view_set.Model_viewset ):
    serializer_class = Package_serializer

    def get_queryset( self ):
        return Package_model.objects.filter(
            partner=self.request.user.partner.get() )


class Check( view_set.Nested_view_set, view_set.mixins.Location_header ):
    def create( self, request, package_pk, format=None ):
        package = Package_model.objects.get( pk=package_pk )
        package.validate( request.data )
        profile = package.create_profile( request.data )
        profile.save()
        sub_profiles, task = package.build_signatures( profile, request.data )
        profile.attach_sub_profiles( sub_profiles )
        profile.save()
        task.delay()

        serializer = Profile_serializer(
            profile, context={ 'request': request } )
        headers = self.get_success_headers( serializer.data )
        return Response( status=status.HTTP_201_CREATED, headers=headers )


class Profile( view_set.Nested_view_set ):
    def retrieve( self, request, pk, format=None ):
        profile = Profile_model.get( pk )
        return Response( profile.to_dict(), status=status.HTTP_200_OK )
