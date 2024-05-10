import io

from company import serializers, models
from django.test import TestCase
from company.tests.mocks.mock_request import MockRequest
from unittest_parametrize import ParametrizedTestCase, parametrize
from rest_framework.exceptions import ValidationError
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile


class ProjectSerializerTestCase(TestCase, ParametrizedTestCase):
    fixtures = ["projectcategory.json", "project.json"]

    def tearDown(self) -> None:
        for project in models.Project.objects.all():
            project.icon.delete()

        return super().tearDown()

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

    @parametrize(
        ("data,failed"),
        (
            ({"name": "Name updated"}, False),
            ({"description": "Description updated"}, False),
            (
                {
                    "name": "Name updated",
                    "category": {"name": "Category name updated"},
                },
                False,
            ),
            ({}, False),
        ),
    )
    def test_write_serializer_update(self, data, failed):
        project = models.Project.objects.get(pk=1)
        request = MockRequest(method="PATCH")

        serializer = serializers.ProjectWriteSerializer(
            instance=project, data=data, context={"request": request}, partial=True
        )

        if failed:
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            project.refresh_from_db()

            for data_k, data_v in data.items():
                if data_k == "category":
                    for data_category_k, data_category_v in data_v.items():
                        category_v = getattr(project.category, data_category_k)
                        self.assertEqual(category_v, data_category_v)
                else:
                    project_v = getattr(project, data_k)
                    self.assertEqual(project_v, data_v)

    @parametrize(
        "image_mode,extension,file_name",
        (("RGB", "JPEG", "file.jpg"), ("RGBA", "PNG", "file.png")),
    )
    def test_project_icon_update_success(self, image_mode, extension, file_name):
        image = io.BytesIO()
        Image.new(image_mode, (100, 100)).save(image, extension)
        image.seek(0)

        file = SimpleUploadedFile(file_name, image.getvalue())
        data = {"icon": file}

        project_pk = 1
        project = models.Project.objects.get(pk=project_pk)
        project.icon.delete()

        serializer = serializers.ProjectIconWriteSerializer(instance=project, data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        project.refresh_from_db()

        self.assertEqual(project.icon.name, f"projects/{file_name}")

    def test_project_icon_update_fail(self):
        project_pk = 1
        project = models.Project.objects.get(pk=project_pk)
        project.icon.delete()
        file = (ContentFile(b"...content...", "icon.txt"),)

        data = {"icon": file}

        serializer = serializers.ProjectIconWriteSerializer(instance=project, data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            self.assertFalse(project.icon)
