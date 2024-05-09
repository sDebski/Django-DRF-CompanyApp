from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import MagicMock
from django.core.files.images import ImageFile

User = get_user_model()


class ProjectViewSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = ["user.json", "projectcategory.json", "project.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    # @parametrize(
    #     "payload,status_",
    #     [
    #         (
    #             {
    #                 "name": "project_1",
    #                 "description": "Description_1",
    #                 "category": {"name": "New category"},
    #             },
    #             status.HTTP_201_CREATED,
    #         ),
    #         (
    #             {
    #                 "name": "project_1",
    #                 "category": {"name": "New category"},
    #             },
    #             status.HTTP_201_CREATED,
    #         ),
    #         ({"name": ""}, status.HTTP_400_BAD_REQUEST),
    #         ({}, status.HTTP_400_BAD_REQUEST),
    #         (
    #             {
    #                 "description": "Description_1",
    #                 "category": {"name": "New category"},
    #             },
    #             status.HTTP_400_BAD_REQUEST,
    #         ),
    #     ],
    # )
    # def test_project_create(self, payload, status_):
    #     url = reverse("company:projects-list")
    #     response = self.client.post(url, data=payload, format="json")

    #     if status_ == status.HTTP_201_CREATED:
    #         project = models.Project.objects.filter(name=payload["name"]).first()
    #         self.assertEqual(project.name, payload["name"])
    #         self.assertEqual(
    #             project.description, payload.get("description")
    #         )  # can be None
    #         self.assertEqual(project.category.name, payload["category"]["name"])
    #     else:
    #         self.assertEqual(response.status_code, status_)

    # def test_project_list(self):
    #     url = reverse("company:projects-list")
    #     response = self.client.get(url)
    #     projects = models.Project.objects.all().order_by("-created_at")
    #     self.assertEqual(len(response.data), projects.count())
    #     serializer = serializers.ProjectReadSerializer(projects, many=True)
    #     projects_data = serializer.data

    #     for response_project, db_project in zip(projects_data, response.data):
    #         with self.subTest(msg="test each project"):
    #             response_project.pop("icon")
    #             db_project.pop("icon")
    #             self.assertDictEqual(response_project, db_project)

    # @parametrize(
    #     "payload,status_",
    #     [
    #         ({"name": "Project_name - updated"}, status.HTTP_200_OK),
    #         ({"descrption": "Description - updated"}, status.HTTP_200_OK),
    #         ({"name": 1234}, status.HTTP_200_OK),
    #         ({"category": {"name": "category - updated"}}, status.HTTP_200_OK),
    #         ({"name": ""}, status.HTTP_400_BAD_REQUEST),
    #         ({"category": ""}, status.HTTP_400_BAD_REQUEST),
    #     ],
    # )
    # def test_project_update(self, payload, status_):
    #     project_pk = 1
    #     url = reverse("company:projects-detail", kwargs={"pk": project_pk})
    #     response = self.client.patch(url, data=payload, format="json")

    #     if status_ == status.HTTP_200_OK:
    #         project = models.Project.objects.get(pk=project_pk)
    #         if "name" in payload:
    #             self.assertEqual(project.name, str(payload["name"]))
    #         if "description" in payload:
    #             self.assertEqual(project.description, payload["description"])
    #         if "category" in payload:
    #             self.assertEqual(project.category.name, payload["category"]["name"])

    #     else:
    #         self.assertEqual(response.status_code, status_)

    @parametrize("file_name, status_", (
            ("file.png", status.HTTP_200_OK),
            ("file.jpg", status.HTTP_200_OK),
            ("file.txt", status.HTTP_400_BAD_REQUEST)
    ))
    def test_project_icon_create(self, file_name, status_):
        file = MagicMock(spec=ImageFile, name=file_name)
        # file = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        project_pk = 1
        url = reverse("company:projects-icon", kwargs={"pk": project_pk })

        data = {
            "icon": file,
        }

        response = self.client.patch(url, data=data, format="multipart")
        if status_ == status.HTTP_200_OK:
            import pdb
            pdb.set_trace()

        else:
            pass




