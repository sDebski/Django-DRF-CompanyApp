from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from company import serializers


class LabelViewset(ModelViewSet):
    authentication_classes = [IsAuthenticated,]
    serializer_class = serializers.LabelSerializer