from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Task, Identifier


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = []
        depth = 2


