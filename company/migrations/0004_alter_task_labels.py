# Generated by Django 3.2 on 2024-05-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0003_alter_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                blank=True, related_name="task_labels", to="company.Label"
            ),
        ),
    ]