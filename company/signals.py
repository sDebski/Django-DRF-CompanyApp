from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from company import attr_handler, models, date_modifier
import os


@receiver(post_save, sender=models.Task)
def modify_expiration_dates(instance, created, **kwargs):
    """
    Modify or not the expiration dates based on status changes
    (*) - Reset both exp dates if created or came back from 'Porzucone' to 'W trakcie'
    (*) - Add 'action days' to both exp dates when 'Zakończone' status set
    (*) - Do not modify if 'Porzucone' or 'Zakończone' status
    (*) - In other cases: Add 'action days' to expired_at depending on upper limit date
    """

    DM = date_modifier.DateModifier
    AH = attr_handler.AttrHandler(instance, "status")

    action_days: int = int(os.environ.get("TASK_BUSY_DAYS_TO_ADD_ON_ACTION", 20))
    limit_days: int = int(os.environ.get("TASK_UPPER_LIMIT_OF_BUSY_DAYS", 60))
    current_local_time: datetime = datetime.now()

    if created or (
        AH.has_field_changed()
        and AH.has_field_previous_values("Porzucone")
        and AH.has_field_current_values("W trakcie")
    ):
        update_data = {
            "expired_at": DM.get_future_date(current_local_time, action_days),
            "maximum_expired_at": DM.get_future_date(current_local_time, limit_days),
        }
    elif AH.has_field_changed() and AH.has_field_current_values("Zakończone"):
        exp_date = DM.get_future_date(current_local_time, action_days)
        update_data = {"expired_at": exp_date, "maximum_expired_at": exp_date}

    elif AH.has_field_current_values("Porzucone", "Zakończone"):
        return

    else:
        update_data = {
            "expired_at": (
                DM.get_future_date_with_limit_date(
                    current_local_time,
                    action_days,
                    instance.maximum_expired_at,
                )
            )
        }

    # to avoid recursive loop with post_save
    models.Task.objects.filter(pk=instance.pk).update(**update_data)
    return
