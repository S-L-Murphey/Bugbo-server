from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User #pylint: disable=imported-auth-user
from bugboapi.models import Employee, UserType

class EmployeeView(ViewSet):
    def list(self, request):

        type = self.request.query_params.get('type', None)
        if type is not None:
            bugbo_employees = Employee.objects.filter(type__id=type)
        else:
            bugbo_employees = Employee.objects.all()
        
        serializer = EmployeeSerializer(
            bugbo_employees, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            bugbo_employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(
                bugbo_employee, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'name', 'description')


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    user_type = UserTypeSerializer(many=False)

    class Meta:
        model = Employee
        fields = ('id', 'bio', 'avatar', 'user', 'user_type')
