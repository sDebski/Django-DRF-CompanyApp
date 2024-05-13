from rest_framework.test import APITestCase
from rest_framework import status
from company import serializers, models
from unittest_parametrize import ParametrizedTestCase, parametrize
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models as django_models
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
                    "title": "Task_title",
                    "description": "task_description",
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
            
        ],
    )
    def test_project_create(self, payload, status_):
        url = reverse("company:tasks-list")
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status_)

        if status_ == status.HTTP_201_CREATED:
            task = models.Task.objects.filter(title=payload["title"]).first()
            self.assertEqual(task.title, payload["title"])
            self.assertEqual(task.status, payload.get("status", "Nowe"))
            self.assertEqual(task.assigned_to.pk, payload["assigned_to"])
            self.assertEqual(task.project.pk, payload["project"])
            self.assertEqual(task.description, payload["description"])
            if payload.get("labels"):
                self.assertTrue(task.labels)
            self.assertTrue(task.created_at)

    def test_task_list(self):
        url = reverse("company:tasks-list")
        response = self.client.get(url)
        tasks = models.Task.objects.all().order_by("-created_at")
        self.assertEqual(len(response.data), tasks.count())
        serializer = serializers.TaskReadSerializer(tasks, many=True)
        serializer_tasks_data = serializer.data

        for serializer_task, response_task in zip(serializer_tasks_data, response.data):
            with self.subTest(msg="test each task"):
                self.assertEqual(serializer_task["title"], response_task["title"])
                self.assertEqual(serializer_task.get("status", "Nowe"), response_task.get("status", "Nowe"))
                self.assertEqual(serializer_task["assigned_to"]["username"], response_task["assigned_to"]["username"])
                self.assertEqual(serializer_task["project"]["name"], response_task["project"]["name"])
                self.assertEqual(serializer_task["description"], response_task["description"])

    @parametrize(
        ("data,status_"),
        (
            ({"title": "Title updated"}, status.HTTP_200_OK),
            ({"description": "Description updated"}, status.HTTP_200_OK),
            (
                {
                    "status": "Zakończone",
                    "assigned_to": 2,
                },
                status.HTTP_200_OK,
            ),
            ({}, status.HTTP_200_OK),
            ({"project": 2137}, status.HTTP_400_BAD_REQUEST),
            ({"assigned_to": 2137}, status.HTTP_400_BAD_REQUEST),
            ({"labels": 1}, status.HTTP_400_BAD_REQUEST),
            ({"status": "Nieistniejący status"}, status.HTTP_400_BAD_REQUEST),
        ),
    )
    def test_write_serializer_update(self, data, status_):
        task_pk = 1
        url = reverse("company:tasks-detail", kwargs={"pk": task_pk})
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status_)

        if status_ == status.HTTP_200_OK:
            task = models.Task.objects.get(pk=task_pk)
            for data_k, data_v in data.items():
                task_v = getattr(task, data_k)

                if isinstance(task_v, django_models.Model):
                    task_v = task_v.pk

                self.assertEqual(task_v, data_v)
