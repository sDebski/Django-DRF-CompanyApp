from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TaskViewSetTestCase(APITestCase, ParametrizedTestCase):
    fixtures = [
        "user.json",
        "projectcategory.json",
        "project.json",
        "label.json",
        "worker.json",
        "task.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    @parametrize(
        "payload,status_",
        [
            (
                {
                    "title": "Task_title",
                    "description": "task_desciption",
                    "status": "Nowe",
                    "project": 1,
                    "assigned_to": 1,
                    "labels": [1],
                },
                status.HTTP_201_CREATED,
            ),
            (
                {
                    "title": "Task_title 2",
                    "description": "task_description 2",
                    "status": "Zakończone",
                    "project": 2,
                    "assigned_to": 2,
                },
                status.HTTP_201_CREATED,
            ),
            (
                {
                    "title": "title",
                    "description": "Description",
                    "status": "Nowe",
                    "project": 2137,
                    "assinged_to": 2137,
                    "labels": [1],
                },
                status.HTTP_400_BAD_REQUEST,
            ),
            ({}, status.HTTP_400_BAD_REQUEST),
            (
                {
                    "title": "Task_title",
                    "description": "task_description",
                    "project": 2,
                    "assigned_to": 2,
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_project_create(self, payload, status_):
        url = reverse("company:tasks-list")
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status_)

        if status_ == status.HTTP_201_CREATED:
            task = models.Task.objects.filter(title=payload["title"]).first()
            self.assertEqual(task.title, payload["title"])
            self.assertEqual(task.status, payload["status"])
            self.assertEqual(task.assigned_to.pk, payload["assigned_to"])
            self.assertEqual(task.project.pk, payload["project"])
            self.assertEqual(task.description, payload["description"])
            if payload.get("labels"):
                self.assertTrue(task.labels)
            self.assertTrue(task.created_at)
            

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
