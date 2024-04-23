# Create your models here.
from django.db import models


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
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="projects/", null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("Nowe", "Nowe"),
        ("W trakcie", "W trakcie"),
        ("Zakończone", "Zakończone"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Nowe")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Worker, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # Zwraca pierwsze 50 znaków komentarza
