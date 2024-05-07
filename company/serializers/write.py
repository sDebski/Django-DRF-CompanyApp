from rest_framework import serializers
from company import models


class LabelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = "name",