"""View module for handling requests about bugs"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Q
from bugboapi.models import Bug, BugType, Employee, BugStatus, BugPriority
from rest_framework.permissions import DjangoModelPermissions

class BugView(ViewSet):
    """Bugbo bugs/tikcets"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = Bug.objects.none()

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized bug/ticket instance
        """
        # Uses the token passed in the `Authorization` header
        employee = Employee.objects.get(user=request.auth.user)
        bug_priority = BugPriority.objects.get(pk=request.data["priority"])
        bug_type = BugType.objects.get(pk=request.data["type"])
        #bug_owner = BugType.objects.get(pk=request.data["owner"])

        # Create a new Python instance of the Bug class
        # and set its properties from what was sent in the
        # body of the request from the client.
        bug = Bug()
        bug.title = request.data["title"]
        bug.description = request.data["description"]
        bug.entry_date = request.data["entry_date"]
        bug.creator = employee
        bug.priority = bug_priority
        bug.type = bug_type
        #bug.owner = bug_owner

        try:
            bug.save()

            bug.tags.set(request.data["tags"])
            serializer = BugSerializer(bug, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single bug/ticket

        Returns:
            Response -- JSON serialized bug instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/bugs/2
            #
            # The `2` at the end of the route becomes `pk`
            bug = Bug.objects.get(pk=pk)
            serializer = BugSerializer(bug, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a bug/ticket

        Returns:
            Response -- Empty body with 204 status code
        """
        employee = Employee.objects.get(user=request.auth.user)
        bug_status = BugStatus.objects.get(pk=request.data["status"])
        bug_priority = BugPriority.objects.get(pk=request.data["priority"])
        bug_type = BugType.objects.get(pk=request.data["type"])
        bug_owner = Employee.objects.get(pk=request.data["owner"])

        bug = Bug.objects.get(pk=pk)
        bug.title = request.data["title"]
        bug.description = request.data["description"]
        bug.entry_date = request.data["entry_date"]
        bug.creator = employee
        bug.status = bug_status
        bug.priority = bug_priority
        bug.type = bug_type
        bug.owner = bug_owner
        bug.save()
        bug.tags.set(request.data["tags"])

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single bug/ticket

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            bug = Bug.objects.get(pk=pk)
            bug.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Bug.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to bugs resource

        Returns:
            Response -- JSON serialized list of bugs
        """
        # Get all game records from the database
        bugs = Bug.objects.all()

        # Support filtering bugs by type
        #    http://localhost:8000/bugs?type=1
        type = self.request.query_params.get('type', None) #pylint: disable=redefined-builtin
        if type is not None:
            bugs = bugs.filter(type__id=type)
        
        # Support filtering bugs by creator
        #    http://localhost:8000/bugs?creator=1
        creator = self.request.query_params.get('creator', None)
        if creator is not None:
            bugs = bugs.filter(creator__id=creator)
        

        # Support filtering bugs by owner
        #    http://localhost:8000/bugs?owner=1
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            bugs = bugs.filter(owner__id=owner)
        

        serializer = BugSerializer(
            bugs, many=True, context={'request': request})
        return Response(serializer.data)

    def search(self, request):
        """Handle Get requests to bugs resource by title search

        Returns:
            Response -- JSON serialized list of bugs/tickets which match the search text
        """
        search_text = self.request.query_params.get('q', None)

        bugs = Bug.objects.filter(
            Q(title__contains=search_text)
        )

        serializer = BugSerializer(
            bugs, many=True, context={'request': request})
        return Response(serializer.data)


class BugSerializer(serializers.ModelSerializer):
    """JSON serializer for bugs

    Arguments:
        serializer type
    """
    class Meta:
        model = Bug
        fields = ('id', 'title', 'description', 'entry_date', 'creator', 'status', 'priority', 'type', 'owner', 'tags')
        depth = 2