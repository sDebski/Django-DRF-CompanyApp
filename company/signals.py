from django.db.models.signals import post_save
from django.dispatch import receiver

from company import models, history_log_creator
