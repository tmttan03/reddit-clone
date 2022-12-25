from rest_framework import serializers

from reddit.users.api.serializers import UserSerializer
from ..models import Todo


class TodoSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = ["id", "title", "author", "status"]

