from rest_framework.test import APITestCase
from company.models import Project, Worker, Task
from django.core.management import call_command
from freezegun import freeze_time

from datetime import datetime


class UpdateStatusesTestCase(APITestCase):
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

    def _check_task_set_up(self):
        self.assertEqual(datetime.now().date(), self.task.expired_at.date())
        self.assertIn(self.task.status, ["Nowe", "W trakcie"])

    @freeze_time("2024-04-17 12:00:00")
    def test_update_status_only_expired_at_crossed(self):
        self._check_task_set_up()
        call_command("update_statuses")

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Zakończone")

    @freeze_time("2024-04-17 12:00:00")
    def test_update_status_maximum_expired_at_crossed(self):
        self._check_task_set_up()

        # Update via qs to avoid triggering post_save signal
        Task.objects.filter(pk=self.task.pk).update(
            maximum_expired_at=self.task.expired_at
        )
        self.task.refresh_from_db()

        self.assertEqual(datetime.now().date(), self.task.maximum_expired_at.date())

        call_command("update_statuses")

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Zamknięte")
