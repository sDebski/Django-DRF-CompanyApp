from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management import call_command
from company import models


User = get_user_model()


class Command(BaseCommand):
    help = "This is a command populating database and creating admin user"

    fixtures = [
        "label.json",
        "worker.json",
        "projectcategory.json",
        "project.json",
        "task.json",
        "comment.json",
    ]

    def create_admin_user(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin")
            self.stdout.write(self.style.SUCCESS("Admin created."))
            return
        self.stdout.write(self.style.SUCCESS("Admin user exists."))

    def handle(self, *args, **kwargs):
        self.create_admin_user()

        database_populated = models.Project.objects.all().exists()
        if database_populated:
            return

        for fixture in self.fixtures:
            call_command("loaddata", fixture)
        self.stdout.write(self.style.SUCCESS("Database populated."))
