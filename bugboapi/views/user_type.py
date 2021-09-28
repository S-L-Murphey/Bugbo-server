"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError
from bugboapi.models import UserType
from rest_framework.permissions import DjangoModelPermissions

class UserTypeView(ViewSet):
    """Bugbo User Types"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = UserType.objects.none()

    def list(self, request):
        """Handle GET requests to get all user types

        """
        user_types = UserType.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = UserTypeSerializer(
            user_types, many=True, context={'request': request})
        return Response(serializer.data)

class UserTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for user types

    Arguments:
        serializers
    """
    class Meta:
        model = UserType
        fields = ('id', 'name', 'description')