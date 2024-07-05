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
        fields = ("pk", "name", "description", "category", "created_at", "icon")
        extra_kwargs = {
            "pk": {"read_only": True},
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


class TaskReadSerializer(serializers.ModelSerializer):
    project = ProjectReadSerializer()
    assigned_to = WorkerReadSerializer()
    labels = LabelReadSerializer(many=True)

    class Meta:
        model = models.Task
        fields = (
            "pk",
            "title",
            "description",
            "status",
            "project",
            "created_at",
            "assigned_to",
            "labels",
        )
        extra_kwargs = {
            "pk": {"read_only": True},
            "title": {"read_only": True},
            "description": {"read_only": True},
            "status": {"read_only": True},
            "project": {"read_only": True},
            "created_at": {"read_only": True},
            "assigned_to": {"read_only": True},
            "labels": {"read_only": True},
        }
