from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskTypeSearchForm,
    PositionSearchForm,
    WorkerSearchForm,
    TaskSearchForm,
    TaskForm,
)
from task_manager.models import Position, TaskType


class FormsTest(TestCase):
    def test_worker_creation_form_is_valid(self):
        position = Position.objects.create(name="test_position")
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first_name",
            "last_name": "test last_name",
            "position": position
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update_form_is_valid(self):
        position = Position.objects.create(name="test_position")
        form_data = {
            "username": "new_user",
            "first_name": "test first_name",
            "last_name": "test last_name",
            "position": position,
            "email": "test@gmail.com"
        }
        form = WorkerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TaskTypeSearchFormTest(TestCase):
    def test_task_type_search_form_rendering(self):
        form = TaskTypeSearchForm()
        expected_html = (
            "<input type='text' name='name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_name'>"
        )
        self.assertHTMLEqual(str(form["name"]), expected_html)

    def test_task_type_search_form_validation(self):
        form_data = {
            "name": "bug"
        }
        form = TaskTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PositionSearchFormTest(TestCase):
    def test_position_search_form_rendering(self):
        form = PositionSearchForm()
        expected_html = (
            "<input type='text' name='name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_name'>"
        )
        self.assertHTMLEqual(str(form["name"]), expected_html)

    def test_position_search_form_validation(self):
        form_data = {
            "name": "developer"
        }
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class WorkerSearchFormTest(TestCase):
    def test_worker_search_form_rendering(self):
        form = WorkerSearchForm()
        expected_html = (
            "<input type='text' name='username' "
            "placeholder='Search by username' maxlength='255' "
            "id='id_username'>"
        )
        self.assertHTMLEqual(str(form["username"]), expected_html)

    def test_worker_search_form_validation(self):
        form_data = {
            "username": "admin"
        }
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TaskSearchFormTest(TestCase):
    def test_task_search_form_rendering(self):
        form = TaskSearchForm()
        expected_html = (
            "<input type='text' name='name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_name'>"
        )
        self.assertHTMLEqual(str(form["name"]), expected_html)

    def test_task_search_form_validation(self):
        form_data = {
            "name": "fix bug"
        }
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TaskFormTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="test_position")
        self.task_type = TaskType.objects.create(name="test_task_type")
        self.worker1 = get_user_model().objects.create_user(
            username="worker_1",
            password="test_worker_1",
            position=position,
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker_2",
            password="test_worker_2",
            position=position,
        )

    def test_task_creation_form_valid(self):
        workers = get_user_model().objects.filter(
            id__in=[self.worker1.id, self.worker2.id]
        )
        form_data = {
            "name": "test",
            "description": "test_description",
            "deadline": datetime.today().date() + timedelta(days=2),
            "is_completed": "",
            "priority": "medium",
            "task_type": self.task_type,
            "assignees": workers
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        self.assertEqual(str(form.cleaned_data), str(form_data))
