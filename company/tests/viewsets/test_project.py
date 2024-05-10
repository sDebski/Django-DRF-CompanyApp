from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse
import io

from PIL import Image

User = get_user_model()


class ProjectViewSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = ["user.json", "projectcategory.json", "project.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def tearDown(self) -> None:
        for project in models.Project.objects.all():
            project.icon.delete()
        return super().tearDown()

    @parametrize(
        "payload,status_",
        [
            (
                {
                    "name": "project_1",
                    "description": "Description_1",
                    "category": {"name": "New category"},
                },
                status.HTTP_201_CREATED,
            ),
            (
                {
                    "name": "project_1",
                    "category": {"name": "New category"},
                },
                status.HTTP_201_CREATED,
            ),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({}, status.HTTP_400_BAD_REQUEST),
            (
                {
                    "description": "Description_1",
                    "category": {"name": "New category"},
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_project_create(self, payload, status_):
        url = reverse("company:projects-list")
        response = self.client.post(url, data=payload, format="json")

        if status_ == status.HTTP_201_CREATED:
            project = models.Project.objects.filter(name=payload["name"]).first()
            self.assertEqual(project.name, payload["name"])
            self.assertEqual(
                project.description, payload.get("description")
            )  # can be None
            self.assertEqual(project.category.name, payload["category"]["name"])
        else:
            self.assertEqual(response.status_code, status_)

    def test_project_list(self):
        url = reverse("company:projects-list")
        response = self.client.get(url)
        projects = models.Project.objects.all().order_by("-created_at")
        self.assertEqual(len(response.data), projects.count())
        serializer = serializers.ProjectReadSerializer(projects, many=True)
        projects_data = serializer.data

        for response_project, db_project in zip(projects_data, response.data):
            with self.subTest(msg="test each project"):
                response_project.pop("icon")
                db_project.pop("icon")
                self.assertDictEqual(response_project, db_project)

    @parametrize(
        "payload,status_",
        [
            ({"name": "Project_name - updated"}, status.HTTP_200_OK),
            ({"descrption": "Description - updated"}, status.HTTP_200_OK),
            ({"name": 1234}, status.HTTP_200_OK),
            ({"category": {"name": "category - updated"}}, status.HTTP_200_OK),
            ({"name": ""}, status.HTTP_400_BAD_REQUEST),
            ({"category": ""}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_project_update(self, payload, status_):
        project_pk = 1
        url = reverse("company:projects-detail", kwargs={"pk": project_pk})
        response = self.client.patch(url, data=payload, format="json")

        if status_ == status.HTTP_200_OK:
            project = models.Project.objects.get(pk=project_pk)
            if "name" in payload:
                self.assertEqual(project.name, str(payload["name"]))
            if "description" in payload:
                self.assertEqual(project.description, payload["description"])
            if "category" in payload:
                self.assertEqual(project.category.name, payload["category"]["name"])

        else:
            self.assertEqual(response.status_code, status_)

    def generate_photo_file(self, extension):
        file = io.BytesIO()
        file.name = "file." + extension
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.seek(0)
        return file

    @parametrize(
        "extension, status_",
        (
            ("png", status.HTTP_200_OK),
            ("jpg", status.HTTP_200_OK),
            ("txt", status.HTTP_400_BAD_REQUEST),
        ),
    )
    def test_project_icon_create(self, extension, status_):
        file = self.generate_photo_file(extension)
        project_pk = 1
        models.Project.objects.get(pk=project_pk).icon.delete()
        url = reverse("company:projects-icon", kwargs={"pk": project_pk})

        data = {
            "icon": file,
        }

        response = self.client.patch(url, data=data, format="multipart")
        self.assertEqual(response.status_code, status_)

        project = models.Project.objects.get(pk=project_pk)

        if status_ == status.HTTP_200_OK:
            self.assertTrue(project.icon.name.startswith("projects/file"))
            self.assertTrue(project.icon.name.endswith(extension))
        else:
            self.assertFalse(project.icon)
