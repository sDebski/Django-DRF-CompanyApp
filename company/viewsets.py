from rest_framework.viewsets import ModelViewSet

from company import serializers, models


class LabelViewset(ModelViewSet):
    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer