"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bugboapi.models import BugType


class BugTypeView(ViewSet):
    """Level up bug types"""

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

class BugTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for bug/ticket types

    Arguments:
        serializers
    """
    class Meta:
        model = BugType
        fields = ('id', 'label')