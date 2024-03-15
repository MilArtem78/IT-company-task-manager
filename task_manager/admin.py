from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import Position, Worker, Task, TaskType


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class CarAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("is_completed",)
    search_fields = ("name",)
    list_filter = ("priority",)


admin.site.register(Position)
admin.site.register(TaskType)
admin.site.unregister(Group)
