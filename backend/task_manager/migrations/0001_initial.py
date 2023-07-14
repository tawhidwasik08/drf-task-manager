# Generated by Django 4.1.9 on 2023-07-05 21:12

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("task_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "task_name",
                    models.CharField(max_length=200, verbose_name="Task Name"),
                ),
                (
                    "task_description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Task Description"
                    ),
                ),
                (
                    "task_due_date",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                datetime.date(2023, 7, 5)
                            )
                        ],
                        verbose_name="Due Date",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "High"), (2, "Medium"), (3, "Low")],
                        null=True,
                    ),
                ),
                (
                    "completed",
                    models.BooleanField(
                        default=False, null=True, verbose_name="Completed"
                    ),
                ),
                (
                    "task_assignee",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        related_name="task_assignees",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Task Assignee(s)",
                    ),
                ),
                (
                    "task_creator",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Task Creator",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
                "ordering": ["task_id"],
            },
        ),
        migrations.CreateModel(
            name="TaskComment",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("comment", models.TextField(verbose_name="Comment")),
                (
                    "comment_creator",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "task_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="task_manager.task",
                        verbose_name="Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task Comment",
                "verbose_name_plural": "Task Comments",
                "ordering": ["comment_id"],
            },
        ),
    ]
