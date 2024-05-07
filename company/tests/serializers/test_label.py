from company import serializers, models
from django.test import TestCase
from rest_framework.serializers import ValidationError
from unittest_parametrize import ParametrizedTestCase, parametrize
from company.tests.mocks.mock_request import MockRequest


class LabelSerializerTestCase(TestCase):
    fixtures = ["label.json"]

    def test_read_serializer(self):
        label = models.Label.objects.get(pk=1)

        data = serializers.LabelSerializer(label).data

        self.assertEqual(data["name"], label.name)

    def test_write_serializer(self):
        data = {"name": "label_name"}

        request = MockRequest(method="POST")

        serializer = serializers.LabelSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertTrue(models.Label.objects.filter(name="label_name").exists())
