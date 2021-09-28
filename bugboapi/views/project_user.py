"""View module for handling requests about bug/ticket types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ValidationError
from bugboapi.models import ProjectUser, Project, Employee
from rest_framework.permissions import DjangoModelPermissions


class ProjectUserView(ViewSet):
    """Level up project users"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = ProjectUser.objects.none()

    def create(self, request):
        """Handle POST operations
        """
        project_user = ProjectUser()
        project_user.project = Project.objets.get(pk=request.data["project"])
        project_user.user = Employee.objects.get(pk=request.data["user"])

        try:
            project_user.save()
            serializer = ProjectUserSerializer(project_user, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single bug/ticket type

        Returns:
        Response -- JSON serialized bug/ticket type
        """
        try:
            project_user = ProjectUser.objects.get(pk=pk)
            serializer = ProjectUserSerializer(project_user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all bug/ticket types

        """
        project = self.request.query_params.get('project', None)
        if project is not None:
            project_users = ProjectUser.objects.filter(project__id=project)
        else:
            user = self.request.query_params.get('user', None)
            if user is not None:
                project_users = ProjectUser.objects.filter(user__id=user)
            else:
                project_users = ProjectUser.objects.all()

        serializer = ProjectUserSerializer(
            project_users, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a bug types

        Returns:
            Response -- Empty body with 204 status code
        """
        project_user = ProjectUser.objects.get(pk=pk)
        project_user.project = Project.objets.get(pk=request.data["project"])
        project_user.user = Employee.objects.get(pk=request.data["user"])
        project_user.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single project users

        """
        try:
            project_user = ProjectUser.objects.get(pk=pk)
            project_user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ProjectUserSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False)
    user = EmployeeSerializer(many=False)
    class Meta:
        model = ProjectUser
        fields = '__all__'