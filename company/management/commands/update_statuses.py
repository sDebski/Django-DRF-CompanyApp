from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from company import models
from company.history_log_creator import HistoryLogCreator

User = get_user_model()


class Command(BaseCommand):
    """
    Command updating tasks' statuses.
    """

    def handle(self, *args, **options):
        current_date = timezone.now().date()
        active_tasks = models.Task.objects.filter(
            status__in=["W trakcie", "Nowe"], expired_at__date=current_date
        )
        system_user = User.objects.get_or_create(username="system", email="system@test.com")[0]

        for task in active_tasks:
            task.status = (
                "Zamknięte"
                if task.expired_at == task.maximum_expired_at
                else "Zakończone"
            )
            HistoryLogCreator.create(task=task, user=system_user)

        models.Task.objects.bulk_update(active_tasks, ["status"])

        self.stdout.write(f"Statuses updated.")
