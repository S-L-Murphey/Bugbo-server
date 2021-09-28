"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from bugboapi.models import BugType
from rest_framework.permissions import DjangoModelPermissions


class BugTypeView(ViewSet):
    """Level up bug types"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = BugType.objects.none()

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized bug_type instance
        """
        bug_type = BugType()
        bug_type.label = request.data["label"]

        try:
            bug_type.save()
            serializer = BugTypeSerializer(bug_type, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single bug/ticket type

        Returns:
        Response -- JSON serialized bug/ticket type
        """
        try:
            bug_type = BugType.objects.get(pk=pk)
            serializer = BugTypeSerializer(bug_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all bug/ticket types

        Returns:
            Response -- JSON serialized list of bug/ticket types
        """
        bug_types = BugType.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BugTypeSerializer(
            bug_types, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a bug types

        Returns:
            Response -- Empty body with 204 status code
        """
        bug_type = BugType.objects.get(pk=pk)
        bug_type.label = request.data["label"]
        bug_type.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single bug_types

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            bug_type = BugType.objects.get(pk=pk)
            bug_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BugType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BugTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for bug/ticket types

    Arguments:
        serializers
    """
    class Meta:
        model = BugType
        fields = ('id', 'label')