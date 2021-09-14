from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bugboapi.models import Bug, Tag, BugTag

class BugTagView(ViewSet):
    
    def create(self, request):
        bug_tag = BugTag()
        bug_tag.tag = Tag.objects.get(pk=request.data["tag"])
        bug_tag.bug = Bug.objects.get(pk=request.data["bug"])

        try:
            bug_tag.save()
            serializer = BugTagSerializer(bug_tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        bug_tag = BugTag.objects.get(pk=pk)
        bug_tag.tag = Tag.objects.get(pk=request.data["tag"])
        bug_tag.bug = Bug.objects.get(pk=request.data["bug"])
        bug_tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            bug_tag = BugTag.objects.get(pk=pk)
            serializer = BugTagSerializer(bug_tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            bug_tag = BugTag.objects.get(pk=pk)
            bug_tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            bug_tags = BugTag.objects.filter(tag__id=tag)
        else:
            bug = self.request.query_params.get('bug', None)
            if bug is not None:
                bug_tags = BugTag.objects.filter(bug__id=bug)
            else:
                bug_tags = BugTag.objects.all()

        serializer = BugTagSerializer(
            bug_tags, many=True, context={'request': request}
        )
        return Response(serializer.data)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'

class BugTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)
    bug = BugSerializer(many=False)
    class Meta:
        model = BugTag
        fields = '__all__'