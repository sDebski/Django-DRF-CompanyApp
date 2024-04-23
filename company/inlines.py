from company import models
from django.contrib import admin


class CommentInline(admin.StackedInline):
    model = models.Comment
    fields = ("content", "task")
    readonly_fields = ("task",)
    extra = 1
    max_num = 5


class TaskInline(admin.TabularInline):
    model = models.Task
    fields = (
        "title",
        "status",
        "assigned_to",
    )
    readonly_fields = fields
    can_delete = False
    ordering = ("status",)
    extra = 0
    max_num = 10
