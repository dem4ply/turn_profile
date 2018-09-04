from turn_django import view_set
from rest_framework.permissions import IsAdminUser
from .models import Partner as Partner_model
from .serializers import Partner as Partner_serializer


class Partner( view_set.Model_viewset ):
    permission_classes = [ IsAdminUser ]
    queryset = Partner_model.objects.all()
    serializer_class = Partner_serializer
