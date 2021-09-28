"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from bugboapi.models import BugStatus
from rest_framework.permissions import DjangoModelPermissions


class BugStatusView(ViewSet):
    """Bugbo bug status"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = BugStatus.objects.none()

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized bug_status instance
        """
        bug_status = BugStatus()
        bug_status.name = request.data["name"]

        try:
            bug_status.save()
            serializer = BugStatusSerializer(bug_status, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single status

        Returns:
        Response -- JSON serialized status type
        """
        try:
            bug_status = BugStatus.objects.get(pk=pk)
            serializer = BugStatusSerializer(bug_status, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all status types

        Returns:
            Response -- JSON serialized list of status types
        """
        bug_statuses = BugStatus.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BugStatusSerializer(
            bug_statuses, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a statuses

        Returns:
            Response -- Empty body with 204 status code
        """
        bug_status = BugStatus.objects.get(pk=pk)
        bug_status.name = request.data["name"]
        bug_status.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single statuses

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            bug_status = BugStatus.objects.get(pk=pk)
            bug_status.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BugStatus.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BugStatusSerializer(serializers.ModelSerializer):
    """JSON serializer for status types

    Arguments:
        serializers
    """
    class Meta:
        model = BugStatus
        fields = ('id', 'name')