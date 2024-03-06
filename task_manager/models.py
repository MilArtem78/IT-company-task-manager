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
