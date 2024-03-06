from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from it_company_task_manager.settings import AUTH_USER_MODEL


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        related_name="workers"
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def get_absolute_url(self):
        return reverse(
            "task_manager:worker-detail",
            kwargs={"pk": self.pk}
        )


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
        ("urgent", "Urgent Priority"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        max_length=10,
        default="medium"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name="assigned_tasks"
    )

    def __str__(self):
        return f"{self.name} ({self.priority})"

    def get_absolute_url(self):
        return reverse(
            "task_manager:task-detail",
            kwargs={"pk": self.pk}
        )
