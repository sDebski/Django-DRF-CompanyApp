from rest_framework.test import APITestCase
from company.history_log_creator import HistoryLogCreator
from company import models, serializers
from company.tests.mocks.mock_request import MockRequest
from django.contrib.auth import get_user_model


User = get_user_model()


class HistoryLogTestCase(APITestCase):

    fixtures = [
        "worker.json",
        "label.json",
        "projectcategory.json",
        "user.json",
        "project.json",
        "task.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.task = models.Task.objects.first()
        return super().setUp()

    def test_history_log_on_creation(self):
        self.assertFalse(models.HistoryLog.objects.all().exists())

        HistoryLogCreator.create(task=self.task, user=self.user, created=True)

        history_log = models.HistoryLog.objects.first()
        self.assertTrue(history_log)
        self.assertEqual(len(history_log.actions.all()), 1)

        creation_action = history_log.actions.first()
        self.assertEqual(creation_action.type, "dodanie_zadania")

    def test_history_log_on_modification(self):
        self.assertFalse(models.HistoryLog.objects.all().exists())

        # 1st action
        self.task.title = "History Log Title"
        # 2nd action
        new_worker = models.Worker.objects.get(pk=2)
        self.task.assigned_to = new_worker

        HistoryLogCreator.create(task=self.task, user=self.user)

        history_log = models.HistoryLog.objects.first()
        self.assertTrue(history_log)
        self.assertEqual(len(history_log.actions.all()), 2)

        edycja_tytulu_action = history_log.actions.all()[0]
        self.assertEqual(edycja_tytulu_action.type, "edycja_adresata")

        edycja_adresata_action = history_log.actions.all()[1]
        self.assertEqual(edycja_adresata_action.type, "edycja_tytulu")

    def test_history_log_on_closing(self):
        self.assertFalse(models.HistoryLog.objects.all().exists())

        # 1st action: status change
        # 2nd action: setting 'closing' status
        self.task.status = "Zakończone"
        HistoryLogCreator.create(task=self.task, user=self.user)

        history_log = models.HistoryLog.objects.first()
        self.assertTrue(history_log)
        self.assertEqual(len(history_log.actions.all()), 2)

        edycja_tytulu_action = history_log.actions.all()[0]
        self.assertEqual(edycja_tytulu_action.type, "edycja_statusu")

        edycja_adresata_action = history_log.actions.all()[1]
        self.assertEqual(edycja_adresata_action.type, "zamkniecie_zadania")

    def test_write_serializer_history_log_creation(self):
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
        task = serializer.save()

        history_logs = task.history_logs.all()
        self.assertTrue(history_logs.first())
        self.assertEqual(history_logs.count(), 1)
        self.assertEqual(len(history_logs.first().actions.all()), 1)
        creation_action = history_logs.first().actions.first()

        self.assertEqual(creation_action.type, "dodanie_zadania")

    def test_write_serializer_history_log_modification(self):
        data = {
            "title": "History Log Title",  # edycja tytułu #4
            "description": "History Log Description",  # edycja opisu #2
            "status": "W trakcie",  # edycja statusu #3
            "assigned_to": 2,  # edycja adresata #1
        }
        request = MockRequest(user=self.user, method="PATCH")
        serializer = serializers.TaskWriteSerializer(
            instance=self.task, data=data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        history_log = models.HistoryLog.objects.first()
        self.assertTrue(history_log)
        self.assertEqual(len(history_log.actions.all()), 4)

        self.assertEqual(history_log.actions.all()[0].type, "edycja_adresata")
        self.assertEqual(history_log.actions.all()[1].type, "edycja_opisu")
        self.assertEqual(history_log.actions.all()[2].type, "edycja_statusu")
        self.assertEqual(history_log.actions.all()[3].type, "edycja_tytulu")
