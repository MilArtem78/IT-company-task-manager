from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position, Task, TaskType


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="testposition")
        self.task_type = TaskType.objects.create(name="testtasktype")
        self.task1 = Task.objects.create(
            name="task_1",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
        )
        self.task2 = Task.objects.create(
            name="task_2",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
        )
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_detail_listed(self):
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_task_is_completed_listed(self):
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.task1.is_completed)

    def test_task_search_by_name(self):

        url = reverse("admin:task_manager_task_changelist")

        response = self.client.get(url, {"q": self.task1.name.lower()})

        changelist = response.context['cl']

        self.assertEqual(self.task1.name, changelist.queryset.first().name)
        self.assertNotIn(self.task2, changelist.queryset)

    def test_task_filter_by_name(self):

        url = reverse("admin:task_manager_task_changelist")

        response = self.client.get(url, {"name__exact": self.task1.name})

        changelist = response.context['cl']
        self.assertEqual(self.task1.name, changelist.queryset.first().name)
        self.assertNotIn(self.task2, changelist.queryset)
