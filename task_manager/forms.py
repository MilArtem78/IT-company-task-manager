from datetime import timedelta, datetime, date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task_manager.models import Worker, Task


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "position",
            "email",
        ]


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    is_completed = forms.ChoiceField(
        choices=(
            (False, "Not completed"),
            (True, "Completed")
        ),
        required=False,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                }
            )
        }

    def clean_deadline(self):
        return validate_deadline(self.cleaned_data["deadline"])


def validate_deadline(deadline: date) -> date:
    if deadline < datetime.today().date():
        raise ValidationError("Deadline cannot be in the past!")
    if deadline <= datetime.today().date() + timedelta(days=1):
        raise ValidationError("Deadline cannot be less than one day!")
    return deadline
