from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from task_manager.models import Task, Worker, Position


@login_required
def index(request):

    num_tasks = Task.objects.count()
    num_completed_tasks = Task.objects.filter(is_completed=True).count()
    num_workers = Worker.objects.count()
    num_position = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_position": num_position,
        "num_completed_tasks": num_completed_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)

