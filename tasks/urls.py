from django.urls import path, include
from .views import DeleteTaskAPI, FinishTaskAPI, TasksAPI, GetTasksAPI, EditTasksAPI, GetTasksDayAPI, DeleteTaskAPI
from django.conf.urls import url 

urlpatterns = [
    path('create/', TasksAPI.as_view(), name='task-create'),
    path('get/', GetTasksAPI.as_view(), name='task-get'),
    path('edit/', EditTasksAPI.as_view(), name='task-edit'),
    path('finish/', FinishTaskAPI.as_view(), name='task-finish'),
    path('get-day/', GetTasksDayAPI.as_view(), name='task-get-day'),
    path('delete/', DeleteTaskAPI.as_view(), name='task-delete'),
]

