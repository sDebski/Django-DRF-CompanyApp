from company import serializers, models
from django.db import models as django_models
from django.test import TestCase
from unittest_parametrize import ParametrizedTestCase, parametrize
from rest_framework.exceptions import ValidationError
from company.tests.mocks.mock_request import MockRequest

from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializerTestCase(TestCase, ParametrizedTestCase):
    fixtures = [
        "projectcategory.json",
        "project.json",
        "worker.json",
        "label.json",
        "task.json",
        "user.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.first()
        return super().setUp()

    def test_read_serializer(self):
        task = models.Task.objects.get(pk=1)

        data = serializers.TaskReadSerializer(task).data
        self.assertEqual(data["title"], task.title)
        self.assertEqual(data["description"], task.description)
        self.assertEqual(data["status"], task.status)
        self.assertEqual(data["assigned_to"]["username"], task.assigned_to.username)
        self.assertEqual(data["assigned_to"]["email"], task.assigned_to.email)
        self.assertEqual(data["project"]["name"], task.project.name)
        self.assertEqual(
            data["project"]["category"]["name"], task.project.category.name
        )
        self.assertTrue(data["labels"])

    def test_write_serializer_create(self):
        data = {
            "title": "task_title",
            "description": "task_description",
            "status": "W trakcie",
            "project": 1,
            "assigned_to": 1,
            "labels": [1, 2],
        }

        request = MockRequest(user=self.user, method="POST")
        serializer = serializers.TaskWriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        task = models.Task.objects.filter(title="task_title").first()
        self.assertTrue(task)
        self.assertEqual(data["title"], task.title)
        self.assertEqual(data["description"], task.description)
        self.assertEqual(data["status"], task.status)
        self.assertEqual(data["assigned_to"], task.assigned_to.pk)
        self.assertEqual(data["project"], task.project.pk)
        self.assertTrue(data["labels"])

    @parametrize(
        ("data,failed"),
        (
            ({"title": "Title updated"}, False),
            ({"description": "Description updated"}, False),
            (
                {
                    "status": "Zakończone",
                    "assigned_to": 2,
                },
                False,
            ),
            ({}, False),
            ({"project": 2137}, True),
            ({"assigned_to": 2137}, True),
            ({"labels": 1}, True),
            ({"status": "Nieistniejący status"}, True),
        ),
    )
    def test_write_serializer_update(self, data, failed):
        task = models.Task.objects.get(pk=1)

        request = MockRequest(user=self.user, method="PATCH")
        serializer = serializers.TaskWriteSerializer(
            instance=task, data=data, partial=True, context={"request": request}
        )

        if failed:
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            task.refresh_from_db()

            for data_k, data_v in data.items():
                task_v = getattr(task, data_k)

                if isinstance(task_v, django_models.Model):
                    task_v = task_v.pk

                self.assertEqual(task_v, data_v)
