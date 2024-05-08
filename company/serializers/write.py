from rest_framework import serializers
from company import models


class LabelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ("name",)


class ProjectCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectCategory
        fields = ("name",)


class ProjectWriteSerializer(serializers.ModelSerializer):
    category = ProjectCategoryWriteSerializer()
    
    class Meta:
        model = models.Project
        fields = ("pk", "name", "description", "category", "created_at", "icon")
        extra_kwargs = {
            "pk": {"read_only": True},
        }