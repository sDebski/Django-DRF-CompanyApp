from company.models import Task, Project, Worker
from rest_framework.test import APITestCase
from unittest_parametrize import ParametrizedTestCase, parametrize
from freezegun import freeze_time
from datetime import datetime, timezone


class AttrHandlerTestCase(APITestCase, ParametrizedTestCase):
    fixtures = [
        "user.json",
        "projectcategory.json",
        "project.json",
        "label.json",
        "worker.json",
    ]

    def setUp(self) -> None:
        self._create_task()
        return super().setUp()
    
    @freeze_time("2024-03-20 12:00:00")
    def _create_task(self, **task_data):
        project = Project.objects.get(pk=1)
        worker = Worker.objects.get(pk=1)

        task_data_default = {
            "title": "Spotkanie z klientem",
            "description": "Umówienie spotkania z klientem w celu omówienia wymagań",
            "status": "Nowe",
            "project": project,
            "assigned_to": worker,
        }
        task_data_default.update(**task_data)

        self.task = Task.objects.create(**task_data_default)
        self.task.refresh_from_db()

    def test_expiration_dates_at_creation(self):
        self.assertEqual(
            self.task.created_at, datetime(2024, 3, 20, 12, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(
            self.task.expired_at, datetime(2024, 4, 17, 23, 59, tzinfo=timezone.utc)
        )
        self.assertEqual(
            self.task.maximum_expired_at,
            datetime(2024, 6, 12, 23, 59, tzinfo=timezone.utc),
        )

    @freeze_time("2024-04-20 12:00:00")
    def test_expiration_date_at_modification(self):
        self.task.title = "Nowy tytuł"
        self.task.save()
        self.task.refresh_from_db()

        self.assertEqual(
            self.task.expired_at, datetime(2024, 5, 17, 23, 59, tzinfo=timezone.utc)
        )
        self.assertEqual(
            self.task.maximum_expired_at,
            datetime(2024, 6, 12, 23, 59, tzinfo=timezone.utc),
        )

    @freeze_time("2024-04-20 12:00:00")
    def test_expiration_date_at_modification(self):
        self.task.title = "Nowy tytuł"
        self.task.save()
        self.task.refresh_from_db()

        self.assertEqual(
            self.task.expired_at, datetime(2024, 5, 17, 23, 59, tzinfo=timezone.utc)
        )
        self.assertEqual(
            self.task.maximum_expired_at,
            datetime(2024, 6, 12, 23, 59, tzinfo=timezone.utc),
        )
