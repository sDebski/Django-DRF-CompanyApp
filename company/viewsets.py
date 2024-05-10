from rest_framework import mixins, viewsets, response, status, decorators
from company import serializers, models, filtersets
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


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

    @extend_schema(request=serializers.ProjectIconWriteSerializer)
    @decorators.action(detail=True, methods=["patch"])
    def icon(self, request, pk):
        project = get_object_or_404(models.Project, pk=pk)
        serializer = serializers.ProjectIconWriteSerializer(
            instance=project, data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request

        return context
