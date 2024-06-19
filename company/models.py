# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from model_utils import FieldTracker

User = get_user_model()


class Worker(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="projects/", null=True)

    tracker = FieldTracker()

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("Nowe", "Nowe"),
        ("W trakcie", "W trakcie"),
        ("Porzucone", "Porzucone"),
        ("Zakończone", "Zakończone")
        ("Zamknięte", "Zamknięte"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Nowe")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Worker, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, related_name="task_labels", blank=True)

    expired_at = models.DateTimeField(null=True, blank=True)
    maximum_expired_at = models.DateTimeField(null=True, blank=True)

    tracker = FieldTracker()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # Zwraca pierwsze 50 znaków komentarza


class Action(models.Model):
    class ActionTypeChoices(models.TextChoices):
        DODANIE_ZADANIA = "dodanie_zadania", "Dodanie zadania"
        ZAMKNIECIE_ZADANIA = "zamkniecie_zadania", "Zamknięcie zadania"
        EDYCJA_STATUSU = "edycja_statusu", "Edycja statusu"
        EDYCJA_TYTULU = "edycja_tytulu", "Edycja tytułu"
        EDYCJA_OPISU = "edycja_opisu", "Edycja opisu"
        EDYCJA_ETYKIETY = "edycja_etykiety", "Edycja etykiet"
        EDYCJA_ADRESATA = "edycja_adresata", "Edycja adresata"

    type = models.CharField(max_length=50, choices=ActionTypeChoices.choices)
    # details = {
    #     "label_1": "stary tytuł",
    #     "value_1":  "old_title",
    #     "label_2": "nowy tytuł", # optional
    #     "value_2": "new_title", # optional
    #   }
    details = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["type"]

    def __str__(self):
        return self.get_type_display()


class HistoryLog(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="history_logs"
    )
    actions = models.ManyToManyField(Action, related_name="history_logs")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="history_logs"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user} - {self.created_at.date()}"
