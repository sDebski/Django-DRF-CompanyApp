from celery import shared_task
from django.core.management import call_command


@shared_task
def test_add(x, y):
    return x + y


@shared_task
def update_statuses():
    call_command("update_statuses")
