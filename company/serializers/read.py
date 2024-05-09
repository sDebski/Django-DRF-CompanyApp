from rest_framework import serializers
from company import models


class LabelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ("name",)
        extra_kwargs = {"name": {"read_only": True}}


class ProjectCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ("name",)
        extra_kwargs = {"name": {"read_only": True}}


class ProjectReadSerializer(serializers.ModelSerializer):
    category = ProjectCategoryReadSerializer()

    class Meta:
        model = models.Project
        fields = ("name", "description", "category", "created_at", "icon")
        extra_kwargs = {
            "name": {"read_only": True},
            "description": {"read_only": True},
            "category": {"read_only": True},
            "created_at": {"read_only": True},
            "icon": {"read_only": True},
        }


class WorkerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Worker
        fields = ("username", "email")
        extra_kwargs = {"username": {"read_only": True}, "email": {"read_only": True}}
