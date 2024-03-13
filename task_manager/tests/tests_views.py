from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from task_manager.models import Position, Task, TaskType

POSITION_URL = reverse("task_manager:position-list")
WORKER_URL = reverse("task_manager:worker-list")
TASK_TYPE_URL = reverse("task_manager:task-type-list")
TASK_URL = reverse("task_manager:task-list")


class PublicPositionTest(TestCase):

    def test_login_required(self):
        request = self.client.get(POSITION_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        Position.objects.create(name="test1")
        Position.objects.create(name="test2")

    def test_retrieve_positions(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions),
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_filter_position_list(self):
        filter_value = "test1"
        response = self.client.get(
            f'{POSITION_URL}?{urlencode({"name": filter_value})}'
        )
        positions = Position.objects.filter(
            name__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )


class PublicTaskTypeTest(TestCase):

    def test_login_required(self):
        request = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        TaskType.objects.create(name="test1")
        TaskType.objects.create(name="test2")

    def test_retrieve_task_type(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        tasktypes = TaskType.objects.all()
        print(list(response.context["tasktype_list"]))
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(tasktypes),
        )
        self.assertTemplateUsed(response, "task_manager/tasktype_list.html")

    def test_filter_task_type_list(self):
        filter_value = "test1"
        response = self.client.get(
            f'{TASK_TYPE_URL}?{urlencode({"name": filter_value})}'
        )
        tasktypes = TaskType.objects.filter(
            name__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(tasktypes)
        )


class PublicTaskTest(TestCase):

    def test_login_required(self):
        request = self.client.get(TASK_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        task_type = TaskType.objects.create(name="test_task_type")
        Task.objects.create(
            name="task_1",
            description="Task_1 for testing",
            deadline=datetime.today().date(),
            task_type=task_type,
        )
        Task.objects.create(
            name="task_2",
            description="Task_2 for testing",
            deadline=datetime.today().date(),
            task_type=task_type,
        )

    def test_retrieve_task(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks),
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_filter_task_list(self):
        filter_value = "task_1"
        response = self.client.get(
            f'{TASK_URL}?{urlencode({"name": filter_value})}'
        )
        tasks = Task.objects.filter(
            name__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )


class PublicWorkerTest(TestCase):

    def test_login_required(self):
        request = self.client.get(WORKER_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test123",
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="test_position")

        get_user_model().objects.create(
            username="test2",
            password="test123",
            position=self.position
        )

    def test_create_worker(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first_name",
            "last_name": "test last_name",
            "position": self.position.id
        }
        self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position.id, form_data["position"])

    def test_retrieve_worker(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers),
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_filter_worker_list(self):
        filter_value = "test2"
        response = self.client.get(
            f'{WORKER_URL}?{urlencode({"username": filter_value})}'
        )
        drivers = get_user_model().objects.filter(
            username__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(drivers)
        )
