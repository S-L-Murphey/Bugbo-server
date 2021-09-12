"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from bugboapi.models import BugPriority, bug_priority


class BugPriorityView(ViewSet):
    """Level up bug priorities"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized bug_priority instance
        """
        bug_priority = BugPriority()
        bug_priority.label = request.data["label"]

        try:
            bug_priority.save()
            serializer = BugPrioritySerializer(bug_priority, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single bug_priority

        Returns:
        Response -- JSON serialized bug_priority
        """
        try:
            bug_priority = BugPriority.objects.get(pk=pk)
            serializer = BugPrioritySerializer(bug_priority, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all bug_priority

        Returns:
            Response -- JSON serialized list of bug_priority
        """
        bug_priorities = BugPriority.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BugPrioritySerializer(
            bug_priorities, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a bug priorities

        Returns:
            Response -- Empty body with 204 status code
        """
        bug_priority = BugPriority.objects.get(pk=pk)
        bug_priority.label = request.data["label"]
        bug_priority.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single bug priority

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            bug_priority = BugPriority.objects.get(pk=pk)
            bug_priority.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BugPriority.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BugPrioritySerializer(serializers.ModelSerializer):
    """JSON serializer for bug priorities

    Arguments:
        serializers
    """
    class Meta:
        model = BugPriority
        fields = ('id', 'label')