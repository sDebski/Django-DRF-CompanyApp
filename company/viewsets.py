from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from company import serializers, models, filtersets


class LabelViewset(
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
