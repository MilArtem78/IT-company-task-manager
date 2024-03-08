from django.urls import path

from task_manager.views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    WorkerListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "tasktypes/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "tasktypes/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "tasktypes/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "tasktypes/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
]


app_name = "task_manager"
