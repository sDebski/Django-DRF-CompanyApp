from rest_framework import serializers
from company import models


class LabelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = "name", 
        extra_kwargs = {
            "name": {"read_only": True}
        }


