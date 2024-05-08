from company import serializers, models
from django.test import TestCase
from company.tests.mocks.mock_request import MockRequest


class ProjectCategorySerializerTestCase(TestCase):
    fixtures = ["projectcategory.json"]

    def test_read_serializer(self):
        projectcategory = models.ProjectCategory.objects.get(pk=1)

        data = serializers.ProjectCategoryReadSerializer(projectcategory).data
        self.assertEqual(data["name"], projectcategory.name)

    def test_write_serializer_create(self):
        data = {"name": "projectcategory_name"}

        request = MockRequest(method="POST")

        serializer = serializers.ProjectCategoryWriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertTrue(
            models.ProjectCategory.objects.filter(name="projectcategory_name").exists()
        )

    def test_write_serializer_update(self):
        data = {"name": "updated_projectcategory_name"}
        projectcategory = models.ProjectCategory.objects.get(pk=1)
        request = MockRequest(method="POST")

        serializer = serializers.ProjectCategoryWriteSerializer(
            instance=projectcategory, data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        updated_projectcategory = models.ProjectCategory.objects.filter(
            name="updated_projectcategory_name"
        ).first()
        self.assertTrue(updated_projectcategory)
        self.assertEqual(updated_projectcategory.pk, 1)
