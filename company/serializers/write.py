from rest_framework import serializers
from company import models
from django.db import transaction

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
            "pk": {"read_only": True}
        }

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_serializer = ProjectCategoryWriteSerializer(data=category_data)

        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()

        project = models.Project.objects.create(category=category, **validated_data)

        return project
    
    def update(self, instance, validated_data):
        with transaction.atomic():

            try:
                category_data = validated_data.pop("category")
                category_serializer = ProjectCategoryWriteSerializer(data=category_data)
                category_serializer.is_valid(raise_exception=True)
                category = category_serializer.save()    
                instance.category = category
            except KeyError: 
                pass

            for field, value in validated_data.items():
                setattr(instance, field, value)
                
            instance.save()

        return instance