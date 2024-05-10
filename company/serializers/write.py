from rest_framework import serializers
from company import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class LabelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ("name",)


class ProjectCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectCategory
        fields = ("name",)

    def create(self, validated_data):
        name = validated_data["name"]
        projectcategory = models.ProjectCategory.objects.filter(name=name)

        if projectcategory:
            return projectcategory

        projectcategory = models.ProjectCategory.objects.create(**validated_data)
        return projectcategory


class ProjectWriteSerializer(serializers.ModelSerializer):
    category = ProjectCategoryWriteSerializer()

    class Meta:
        model = models.Project
        fields = ("pk", "name", "description", "category", "created_at", "icon")
        extra_kwargs = {"pk": {"read_only": True}}

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
                category_serializer = ProjectCategoryWriteSerializer(
                    instance=instance.category, data=category_data
                )
                category_serializer.is_valid(raise_exception=True)
                category = category_serializer.save()
                instance.category = category
            except KeyError:
                pass

            for field, value in validated_data.items():
                setattr(instance, field, value)

            instance.save()

        return instance


class WorkerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Worker
        fields = ("username", "email")

    def username_unique_validation(self, username):
        worker = models.Worker.objects.filter(username=username).exists()
        if worker:
            raise ValidationError(
                _(f"Worker with such username already exists: {username}")
            )

    def crete(self, validated_data):
        self.username_unique_validation()

        worker = models.Worker.objects.create(**validated_data)
        return worker


class ProjectIconWriteSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField()

    class Meta:
        model = models.Project
        fields = ("icon",)

    def update(self, instance, validated_data):
        icon = validated_data.pop("icon")

        with transaction.atomic():
            instance.icon = icon
            instance.save()

        return instance


class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ("title",)
