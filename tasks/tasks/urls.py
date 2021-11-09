from django.urls import path, include
from .views import TasksAPI, GetTasksAPI

urlpatterns = [
    path('task-create/', TasksAPI.as_view(), name='task-create'),
    path('task-get/', GetTasksAPI.as_view(), name='task-get'),
]