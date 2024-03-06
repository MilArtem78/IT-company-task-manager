from django.urls import path

from task_manager.views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,

)

urlpatterns = [
    path("", index, name="index"),
    path("tasktypes/", TaskTypeListView.as_view(), name="task-type-list"),
    path("tasktypes/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),


]


app_name = "task_manager"