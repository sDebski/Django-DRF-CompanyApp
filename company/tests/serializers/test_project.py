from company import serializers, models
from django.test import TestCase
from company.tests.mocks.mock_request import MockRequest
from django.utils import timezone

class ProjectSerializerTestCase(TestCase):
    fixtures = ["projectcategory.json", "project.json"]

    def test_read_serializer(self):
        project = models.Project.objects.get(pk=1)

        data = serializers.ProjectReadSerializer(project).data
        self.assertEqual(data["name"], project.name)
        self.assertEqual(data["description"], project.description)
        self.assertEqual(data["category"]["name"], project.category.name)

    def test_write_serializer_create(self):
        project = models.Project.objects.get(pk=1)
        data = {
            "name": "project_name",
            "description": "Project description",
            "category": {"name": "Zarzadzanie dokumentacja"},
        }

        request = MockRequest(method="POST")

        serializer = serializers.ProjectWriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        project = models.Project.objects.filter(name="project_name").first()
        self.assertTrue(project)
        self.assertEqual(data["name"], project.name)
        self.assertEqual(data["description"], project.description)
        self.assertEqual(data["category"]["name"], project.category.name)

    def test_write_serializer_update(self):
        data = {"name": "updated_project_name"}
        project = models.Project.objects.get(pk=1)
        request = MockRequest(method="PATCH")

        serializer = serializers.ProjectWriteSerializer(
            instance=project, data=data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        updated_project = models.Project.objects.filter(
            name="updated_project_name"
        ).first()
        self.assertTrue(updated_project)
        self.assertEqual(updated_project.pk, 1)
