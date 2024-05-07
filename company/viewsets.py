from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from company import serializers, models, filtersets


class LabelViewset(ModelViewSet):
    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer
    filterset_class = filtersets.LabelFilterSet
