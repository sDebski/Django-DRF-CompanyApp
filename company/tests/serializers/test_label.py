from company import serializers, models
from django.test import TestCase
from company.tests.mocks.mock_request import MockRequest


class LabelSerializerTestCase(TestCase):
    fixtures = ["label.json"]

    def test_read_serializer(self):
        label = models.Label.objects.get(pk=1)

        data = serializers.LabelReadSerializer(label).data
        self.assertEqual(data["name"], label.name)

    def test_write_serializer_create(self):
        data = {"name": "label_name"}

        request = MockRequest(method="POST")

        serializer = serializers.LabelWriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertTrue(models.Label.objects.filter(name="label_name").exists())

    def test_write_serializer_update(self):
        data = {"name": "updated_label_name"}
        label = models.Label.objects.get(pk=1)
        request = MockRequest(method="POST")

        serializer = serializers.LabelWriteSerializer(
            instance=label, data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        updated_label = models.Label.objects.filter(name="updated_label_name").first()
        self.assertTrue(updated_label)
        self.assertEqual(updated_label.pk, 1)
