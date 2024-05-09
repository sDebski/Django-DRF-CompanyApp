from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from company import serializers, models, filtersets


class LabelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Label.objects.all()
    filterset_class = filtersets.LabelFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.LabelReadSerializer
        return serializers.LabelWriteSerializer


class ProjectCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.ProjectCategory.objects.all()
    filterset_class = filtersets.ProjectCategoryFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ProjectCategoryReadSerializer
        return serializers.ProjectCategoryWriteSerializer


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        models.Project.objects.select_related("category").all().order_by("-created_at")
    )
    filterset_class = filtersets.ProjectFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ProjectReadSerializer
        return serializers.ProjectWriteSerializer


class WorkerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Worker.objects.all()
    filterset_class = filtersets.WorkerFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.WorkerReadSerializer
        return serializers.WorkerWriteSerializer
