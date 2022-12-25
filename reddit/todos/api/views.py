from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from .serializers import TodoSerializer

from ..models import Todo


class TodoViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):

    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(author=self.request.user)

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            item = serializer.save(author=self.request.user)
            return Response({'id': item.id, 'title': item.title}, status=200)
        return Response(serializer.errors, status=400)

    def put(self, *args, **kwargs):
        try:
            instance = Todo.objects.get(id=self.request.data.get('id'))
        except:
            instance = None

        if instance:
            serializer = self.serializer_class(data=self.request.data, instance=instance)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully updated'}, status=200)
            return Response(serializer.errors, status=400)
        return Response({'message': 'Instance not found'}, status=400)