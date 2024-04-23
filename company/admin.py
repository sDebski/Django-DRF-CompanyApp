from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest

from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.conf import settings


from company import models, inlines


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
    )
    list_editable = ("username",)
    ordering = ("username",)


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "category",
        "tasks",
        "icon_",
    )
    search_fields = ("name",)
    list_per_page = 5
    list_filter = ("category",)
    inlines = (inlines.TaskInline,)

    def tasks(self, obj):
        return obj.task_set.count()

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.annotate(tasks_count=Count("task"))

    tasks.order_admin_field = "tasks_count"

    def get_readonly_fields(self, request, obj):
        return ("name", "icon_") if obj else tuple()

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                    "description",
                )
            },
        ),
        ("Others", {"fields": ("category",)}),
    )

    def icon_(self, obj):
        style = f"""
            width: 64px;
            height: 64px;
            border-radius: 10px;
        """
        icon_html = f"""
            <img src="{settings.MEDIA_URL}{obj.icon.name}" style="{style}" />
        """
        return format_html(icon_html)

    def save_formset(self, request, form, formset, change):
        tasks_data = formset.cleaned_data

        print("CLEANED DATA:", tasks_data)
        print("Row", tasks_data[0])
        for task_data in tasks_data:
            task_data = task_data["id"]
            task_data.description += " *Parent project has been updated!* "
            task_data.save()

        self.message_user(
            request, "Task`s descriptions have been updated", messages.INFO
        )

        return super().save_formset(request, form, formset, change)


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "project",
        "assigned_to",
        "comments",
        "in_project",
    )

    def comments(self, obj):
        return obj.comment_set.count()

    inlines = (inlines.CommentInline,)
    list_per_page = 5
    list_filter = ("labels",)

    fieldsets = (
        ("General", {"fields": ("title", "description", "status")}),
        ("Assigns", {"fields": ("project", "assigned_to")}),
    )

    actions = ("add_comment", "clean_comments", "finished_status")

    def save_model(self, request, obj, form, change):
        if change:
            obj.title += " UPDATED |"

            messages.set_level(request, messages.WARNING)
            self.message_user(
                request,
                f"Task has been updated - changed title via hook.",
                messages.WARNING,
            )

        return super().save_model(request, obj, form, change)

    def in_project(self, obj):
        style = f"""
            width: 64px;
            height: 64px;
            border-radius: 10px;
        """
        icon_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <a href="{reverse('admin:company_project_change', kwargs={"object_id": obj.project.pk})}">
                <img src="{settings.MEDIA_URL}{obj.project.icon.name}" style="{style}" />
            </a>
        </div>
        """
        return format_html(icon_html)

    @admin.action(description="Add dummy comment")
    def add_comment(self, request, queryset):
        if not queryset:
            self.message_user(request, "No tasks has been chosen.", messages.ERROR)
            return

        for task in queryset:
            models.Comment.objects.create(content="Dummy comment", task=task)

        self.message_user(
            request,
            f"Comments were added to {queryset.count()} tasks.",
            messages.SUCCESS,
        )

    @admin.action(description="Clean comments")
    def clean_comments(self, request, queryset):
        self._handle_empty_queryset(request, queryset)

        queryset = queryset.prefetch_related("comment_set")
        for task in queryset:
            task.comment_set.all().delete()

        self.message_user(
            request,
            f"Comments were added to {queryset.count()} tasks.",
            messages.SUCCESS,
        )

    @admin.action(description="Set finished status")
    def finished_status(self, request, queryset):
        self._handle_empty_queryset(request, queryset)

        queryset.update(status="Zakończone")

        self.message_user(
            request,
            f"Status 'Finished' was added to {queryset.count()} tasks.",
            messages.SUCCESS,
        )

    def _handle_empty_queryset(self, request, queryset):
        if not queryset:
            self.message_user(request, "No tasks has been chosen.", messages.ERROR)
            return


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "commented_on")

    def delete_model(self, request, obj):
        messages.set_level(request, messages.WARNING)
        self.message_user(
            request,
            "The comment has been delated - SAD FOR COMMUNICATION",
            messages.WARNING,
        )

        return super().delete_model(request, obj)  # just does obj.delete()

    def commented_on(self, obj):
        a_html = f"""
            <a href="{reverse('admin:company_task_change', kwargs={"object_id": obj.task.pk})}">{obj.task}</a>
        """
        return format_html(a_html)
