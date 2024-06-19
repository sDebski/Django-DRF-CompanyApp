from company import models
from core.models import User


class HistoryLogCreator:
    """
    Class which performs creating history log based on task changes
    """

    closing_statuses = ["Zakończone", "Porzucone"]

    action_types_draft = {
        "status": {
            "type": "edycja_statusu",
            "label_1": "Stary status",
            "label_2": "Nowy status",
        },
        "title": {
            "type": "edycja_tytulu",
            "label_1": "Stary tytuł",
            "label_2": "Nowy tytuł",
        },
        "description": {
            "type": "edycja_opisu",
            "label_1": "Stary opis",
            "label_2": "Nowy opis",
        },
        "assigned_to_id": {
            "type": "edycja_adresata",
            "label_1": "Stary adresat",
            "label_2": "Nowy adresat",
        },
    }

    @staticmethod
    def add_creation_history_log(instance: models.Task, user: User):
        """
        Creates history log with basic creation action
        """
        action_details = {
            "label_1": "Dodano zadanie:",
            "value_1": instance.title,
        }
        action = models.Action.objects.create(
            type="dodanie_zadania", details=action_details
        )
        history_log = models.HistoryLog.objects.create(task=instance, user=user)
        history_log.actions.add(action)
        history_log.save()
        return history_log

    @staticmethod
    def add_history_log_with_actions(
        instance: models.Task, user: User, actions: list[models.Action]
    ):
        """
        Function that creates history log with actions
        """
        if actions:
            history_log = models.HistoryLog.objects.create(task=instance, user=user)
            history_log.actions.add(*[action.pk for action in actions])
            history_log.save()
            return history_log
        return None

    @staticmethod
    def get_closing_status_action(instance):
        """
        Function creates closing action and returns created Action obj.
        """

        action_details = {
            "label_1": "Zamknięto zadanie, Powód:",
            "value_1": f" {instance.status}",
        }
        return models.Action.objects.create(
            type="zamkniecie_zadania", details=action_details
        )

    @classmethod
    def handle_closing_status(cls, key, instance, actions):
        """
        Function checks if the new status in "Zakończone" to perform adding closing action.
        """
        local_actions = actions[:]

        if key == "status" and instance.status in cls.closing_statuses:
            local_actions.append(cls.get_closing_status_action(instance=instance))
            return local_actions
        return local_actions

    @classmethod
    def create(cls, task: models.Task, user: User = None, created=False):
        """
        Creates history log based on task instance and user.
        One can also add info about the task being created or modified.
        Function returns created HistoryLog object or None.
        """
        instance = task
        if created:
            return cls.add_creation_history_log(instance=instance, user=user)

        actions = []
        changes = {**instance.tracker.changed(), **instance.project.tracker.changed()}
        project_fields = instance.project.tracker.changed().keys()
        for key, value in changes.items():
            obj = instance.project if key in project_fields else instance
            if key in ["labels", "expired_at", "maximum_expired_at"]:
                continue
            if key == "assigned_to_id":
                old_value = models.Worker.objects.get(pk=value).username
                new_value = instance.assigned_to.username
            else:
                old_value = value
                new_value = getattr(obj, key)

            action_type = cls.action_types_draft.get(key)
            if not action_type:
                continue
            action_details = {
                "label_1": action_type.get("label_1"),
                "value_1": old_value,
                "label_2": action_type.get("label_2"),
                "value_2": new_value,
            }

            action = models.Action.objects.create(
                type=action_type["type"], details=action_details
            )
            actions.append(action)

            actions = cls.handle_closing_status(
                key=key, instance=instance, actions=actions
            )

        return cls.add_history_log_with_actions(
            instance=instance, actions=actions, user=user
        )
