import time
from django.apps import apps


def calculate_value(value):
    time.sleep(1)
    return int(value) ** 2


def get_models_from_app(app_name: str):
    app_config = apps.get_app_config(app_name)
    return list(app_config.get_models())
