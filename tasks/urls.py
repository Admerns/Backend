from django.urls import path, include
from .views import FinishTaskAPI, TasksAPI, GetTasksAPI, EditTasksAPI, GetTasksDayAPI

urlpatterns = [
    path('task-create/', TasksAPI.as_view(), name='task-create'),
    path('task-get/', GetTasksAPI.as_view(), name='task-get'),
    path('task-edit/', EditTasksAPI.as_view(), name='task-edit'),
    path('task-finish/', FinishTaskAPI.as_view(), name='task-finish'),
    path('task-get-day/', GetTasksDayAPI.as_view(), name='task-get-day'),
]