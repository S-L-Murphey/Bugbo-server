"""View module for handling requests about projects"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User #pylint: disable=imported-auth-user
from bugboapi.models import Project
from rest_framework.permissions import DjangoModelPermissions


class ProjectView(ViewSet):
    """Bugbo projects"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = Project.objects.none()

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized project instance
        """
        # Uses the token passed in the `Authorization` header

        # Create a new Python instance of the Project class
        # and set its properties from what was sent in the
        # body of the request from the client.
        project = Project()
        project.name = request.data["name"]
        project.description = request.data["description"]
        

        try:
            project.save()
            assignees = request.data["assignees"]
            bugs = request.data["bugs"]

            for assignee in assignees:
                project.assignees.add(assignee["id"])

            for bug in bugs:
                project.bugs.add(bug["id"])

            serializer = ProjectSerializer(project, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single project

        Returns:
            Response -- JSON serialized projet instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/bugs/2
            #
            # The `2` at the end of the route becomes `pk`
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a project

        Returns:
            Response -- Empty body with 204 status code
        """
        project = Project.objects.get(pk=pk)
        project.name = request.data["name"]
        project.description = request.data["description"]
        
        project.save()

        project.bugs.set(request.data["bugs"])
        project.assignees.set(request.data["assignees"])

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single project

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            project = Project.objects.get(pk=pk)
            project.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to projects resource

        Returns:
            Response -- JSON serialized list of projects
        """
        # Get all game records from the database
        projects = Project.objects.all()
        
        serializer = ProjectSerializer(
            projects, many=True, context={'request': request})
        return Response(serializer.data)


class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for bugs

    Arguments:
        serializer type
    """

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'assignees', 'bugs')
        depth = 3