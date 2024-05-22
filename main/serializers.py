from rest_framework import serializers
from .models import User, Project, Task, Tag

# Serializer para o modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer para o modelo Project
class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members']

# Serializer para o modelo Task
class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, 
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'creation_date', 'status', 'project', 'tags']

# Serializer para o modelo Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
