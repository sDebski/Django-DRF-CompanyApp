from celery import shared_task
import time


@shared_task
def test_add(x, y):
    return x + y