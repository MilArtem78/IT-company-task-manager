from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Worker, Position, Task, TaskType


class ModelTests(TestCase):
    def test_worker_str(self):
        position = Position.objects.create(name="test_position")
        worker = get_user_model().objects.create_user(
            username="worker",
            password="test_worker",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position})"
        )

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        task = Task.objects.create(
            name="task_1",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=task_type,
        )
        self.assertEqual(
            str(task),
            f"{task.name} ({task.priority})"
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position.objects.create(name="test_position")
        self.assertEqual(str(position), position.name)

    def test_create_worker_with_position(self):
        position = Position.objects.create(name="test_position")
        username = "test"
        password = "test_worker"
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position, position)
        self.assertTrue(worker.check_password(password))
